"""Typed drafts and early new-person shape checks, not identity inference."""
import copy
import re


def new_template(kind):
    if kind not in ('judge', 'clerk'):
        raise ValueError('Choose the evidenced directory role: judge or clerk')
    labels = (('chambers_phone','chambers_address','assistant_name','assistant_contact')
              if kind == 'judge' else ('office_phone','office_address','office_contact'))
    fields = {label:dict(value='',status='unreviewed',citation={}) for label in labels}
    return dict(key='person-<stable-id>', kind=kind, facts=dict(name='', fields=fields),
                citations=[], expected_version=None)


def existing_template(prior):
    if prior['kind'] not in ('judge', 'clerk'):
        raise ValueError('Existing person template requires judge or clerk')
    result = copy.deepcopy({key: prior[key] for key in ('key','kind','facts','expected_version')})
    result['citations'] = []  # Current acquired bindings, not blindly copied history.
    return result


def validate_finding(finding, prior=None):
    # Existing legacy records retain their exact preservation/version contract.
    # Source-gate has checked those guards before calling this helper.
    if prior is not None:
        return
    kind, facts = finding['kind'], finding['facts']
    if kind == 'personnel_change' and facts.get('name'):
        raise ValueError('A new named directory person requires kind judge or clerk and its own person- key; use the returned personnel template')
    if kind not in ('judge','clerk'):
        return
    if not re.fullmatch(r'person-[a-z0-9]+(?:-[a-z0-9]+)*', finding['key']):
        raise ValueError('New judge/clerk requires its own stable person- ID; replace template placeholders')
    name = facts.get('name')
    if not isinstance(name, str) or not name.strip() or '<' in name or '>' in name:
        raise ValueError('New judge/clerk requires the supported full name, not a template placeholder')
    # A missing fields object is permitted for legacy finding compatibility.
    # Blank draft fields must be filled or omitted, never asserted absent by default.
    fields = facts.get('fields', {})
    if not isinstance(fields, dict):
        raise ValueError('Personnel facts.fields must contain named contact objects')
    for label, field in fields.items():
        if not isinstance(field, dict):
            raise ValueError('Personnel contact field must be an object: ' + label)
        citation = field.get('citation')
        if not isinstance(citation, dict) or not citation or citation not in finding['citations']:
            raise ValueError('New contact citation must be included in acquired finding citations: ' + label)
        status = field.get('status')
        if status == 'verified':
            value = field.get('value')
            if not value or (isinstance(value, str) and not value.strip()):
                raise ValueError('Verified contact needs its supported value: ' + label)
        elif status == 'not_published':
            log = field.get('search_log')
            if (not isinstance(log, list) or not log
                    or any(not item or not isinstance(item, (str,dict)) for item in log)):
                raise ValueError('Unpublished contact requires a nonempty cited search_log: ' + label)
        else:
            raise ValueError('New contact must be verified or explicitly not_published with searched evidence; omit unreviewed fields: ' + label)
