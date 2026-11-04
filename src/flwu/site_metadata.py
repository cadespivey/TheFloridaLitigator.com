"""Explicit Circuit 7 request metadata, never whole-script relevance guesses."""
from __future__ import annotations

import base64
import json
import re

from flwu import history as h

NONCES = {
    'ctPublicFunctions': (None, [('_ajax_nonce',), ('_rest_nonce',)]),
    'ctPublic': (None, [('_ajax_nonce',), ('emailEncoderPassKey',), ('ct_checkjs_key',), ('pixel__url',)]),
    'ecs_ajax_params': ('ecs_ajax_load-js-extra', [('nonce',)]),
    'jetMenuPublicSettings': ('jet-menu-public-scripts-js-extra', [('restNonce',)]),
    'elementorFrontendConfig': ('elementor-frontend-js-before', [
        ('nonces', 'floatingButtonsClickTracking'), ('nonces', 'atomicFormsSendForm')]),
    'localize': ('eael-general-js-extra', [('nonce',), ('eael_login_nonce',),
        ('eael_register_nonce',), ('eael_lostpassword_nonce',), ('eael_resetpassword_nonce',)]),
    'ElementorProFrontendConfig': ('elementor-pro-frontend-js-before', [('nonce',)]),
}
PIXEL = re.compile(r'https://moderate[0-9]+-v4\.cleantalk\.org/pixel/[0-9a-f]{32}\.gif')
CF = re.compile(r"window\.__CF\$cv\$params=\{r:'([0-9a-f]{16})',t:'([A-Za-z0-9+/]+={0,2})'\}")


def _unique(pairs):
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError('Duplicate technical JSON key')
    return dict(pairs)


def _constant(value):
    raise ValueError('Non-JSON technical constant')


DECODER = json.JSONDecoder(object_pairs_hook=_unique, parse_constant=_constant)


def normalize(nodes, court):
    """Keep all unrecognized fields, DOM boundaries, attributes and script logic."""
    if not (any(n['tag']=='meta' and n['attrs'].get('name')=='generator'
                and str(n['attrs'].get('content','')).startswith('Elementor ') for n in nodes)
            and any(n['tag']=='link' and 'https://api.w.org/' in n['attrs'].get('rel',[]) for n in nodes)):
        raise ValueError('Unrecognized Circuit 7 WordPress page')
    metadata, components = [], []

    def tracked(prop, value):
        metadata.append(dict(property=prop, value_sha256=h.sha(value)))
        return {'flwu_tracked_metadata': prop}

    def pixel(value):
        if not isinstance(value,str) or not PIXEL.fullmatch(value):
            raise ValueError('Unknown CleanTalk pixel')
        return tracked('cleantalk_pixel', value)

    def nonce(prop, value):
        if prop.endswith('pixel__url'):return pixel(value)
        if prop.endswith('ct_checkjs_key'):
            valid=type(value) is int and 10**7<=value<10**11
        else:
            size=32 if prop.endswith('emailEncoderPassKey') else 10
            valid=isinstance(value,str) and re.fullmatch('[0-9a-f]{'+str(size)+'}',value)
        if not valid:raise ValueError('Unknown technical token format')
        return tracked(prop,value)

    # A JSON assignment is decoded, but its surrounding JavaScript remains exact.
    for node in nodes:
        attrs=node['attrs']
        if node['tag']=='script':
            for child in node['children']:
                text=child.get('value')
                if not isinstance(text,str):continue
                for variable,(script_id,paths) in NONCES.items():
                    pattern=r'\s*var\s+'+variable+r'\s*=\s*'
                    match=re.match(pattern,text)
                    if not match or attrs.get('id')!=script_id:continue
                    parts=[];remaining=text
                    while match:
                        data,end=DECODER.raw_decode(remaining[match.end():])
                        if not isinstance(data,dict):raise ValueError('Unknown technical assignment')
                        for path in paths:
                            parent=data
                            for key in path[:-1]:parent=parent.get(key,{})
                            if not isinstance(parent,dict):raise ValueError('Unknown technical field parent')
                            if path[-1] in parent:
                                prop=variable+'.'+'.'.join(path)
                                parent[path[-1]]=nonce(prop,parent[path[-1]])
                        parts.extend([remaining[:match.end()],h.canonical(data)])
                        remaining=remaining[match.end()+end:]
                        separator=re.match(r';\s*(?=var\s+'+variable+r'\s*=)',remaining)
                        if not separator:break
                        parts.append(separator[0]);remaining=remaining[separator.end():]
                        match=re.match(pattern,remaining)
                    child['value']=''.join(parts)+remaining
                    break
        if node['tag']=='div' and 'jet-mega-menu' in attrs.get('class',[]) and 'data-settings' in attrs:
            settings=DECODER.decode(attrs['data-settings'])
            if not isinstance(settings,dict):raise ValueError('Unknown menu settings')
            if 'menuUniqId' in settings:
                value=settings['menuUniqId']
                if not isinstance(value,str) or not re.fullmatch('[0-9a-f]{13}',value):
                    raise ValueError('Unknown menu request identifier')
                settings['menuUniqId']=tracked('menuUniqId',value)
            attrs['data-settings']=settings
        if (node['tag']=='img' and attrs.get('id')=='apbct_pixel'
                and attrs.get('alt')==attrs.get('title')=='Cleantalk Pixel'):
            attrs['src']=pixel(attrs.get('src'))

    wrappers=[n for n in nodes if n['tag']=='div' and 'gtranslate_wrapper' in n['attrs'].get('class',[])]
    for number,wrapper in enumerate(wrappers):
        match=re.fullmatch(r'gt-wrapper-([0-9]{8})',str(wrapper['attrs'].get('id','')))
        if not match:raise ValueError('Unknown translation wrapper')
        token=match[1];marker='FLWU_GT_'+str(number)
        scripts=[n for n in nodes if n['tag']=='script' and n['attrs'].get('id')=='gt_widget_script_'+token+'-js-before']
        external=[n for n in nodes if n['tag']=='script' and n['attrs'].get('data-gt-widget-id')==token]
        if len(scripts)!=1 or len(external)!=1 or len(scripts[0]['children'])!=1:
            raise ValueError('Unbound translation references')
        child=scripts[0]['children'][0];text=child.get('value','')
        prefix="\nwindow.gtranslateSettings = /* document.write */ window.gtranslateSettings || {};window.gtranslateSettings['"+token+"'] = "
        suffix=';\n//# sourceURL=gt_widget_script_'+token+'-js-before\n'
        if not text.startswith(prefix) or not text.endswith(suffix):raise ValueError('Unknown translation script')
        settings=DECODER.decode(text[len(prefix):-len(suffix)])
        if not isinstance(settings,dict) or settings.get('wrapper_selector')!='#gt-wrapper-'+token:
            raise ValueError('Unknown translation configuration')
        settings['wrapper_selector']='#gt-wrapper-'+marker
        child['value']=prefix.replace(token,marker)+h.canonical(settings)+suffix.replace(token,marker)
        wrapper['attrs']['id']='gt-wrapper-'+marker
        scripts[0]['attrs']['id']='gt_widget_script_'+marker+'-js-before'
        external[0]['attrs']['data-gt-widget-id']=marker
        tracked('gtranslate_widget_id',token)

    for node in nodes:
        if node['tag']!='script':continue
        for child in node['children']:
            text=child.get('value')
            if not isinstance(text,str) or 'window.__CF$cv$params=' not in text:continue
            matches=list(CF.finditer(text))
            if (len(matches)!=1 or not text.startswith('(function(){function c(){')
                    or '/cdn-cgi/challenge-platform/scripts/jsd/main.js' not in text):
                raise ValueError('Unknown Cloudflare wrapper')
            match=matches[0];ray,encoded=match.groups();decoded=base64.b64decode(encoded,validate=True)
            if len(decoded)!=10 or not decoded.isdigit() or base64.b64encode(decoded).decode()!=encoded:
                raise ValueError('Unknown challenge timestamp')
            normalized=text[:match.start()]+"window.__CF$cv$params={r:'FLWU_RAY',t:'FLWU_TIME'}"+text[match.end():]
            normalized=normalized.replace('/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray='+ray,
                                          '/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=FLWU_RAY')
            tracked('cloudflare_request',dict(ray=ray,time=encoded))
            # Changed challenge logic still needs one completed same-court review.
            components.append(dict(court=court,kind='cloudflare_challenge',sha256=h.sha(normalized),location='script'))
            child['value']={'flwu_shared_component':'cloudflare_challenge'}
    return metadata,components
