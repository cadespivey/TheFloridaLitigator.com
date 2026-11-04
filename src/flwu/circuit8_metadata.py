"""Bounded WPBakery identity bindings and separately reviewed release assets.

Never discard CSS/JS versions or assume an asset target's bytes are unchanged.
Exact resource URLs and CMS versions remain shared reviewable components.
"""
from __future__ import annotations

import json
import re
from urllib.parse import urlsplit

from flwu import history as h
from flwu.site_metadata import DECODER

ASSETS = {
    'svc-front-css-css': '/wp-content/plugins/svc-post-grid-addon/assets/css/front.css',
    'svc-fontawosem-css-css': '/wp-content/plugins/svc-post-grid-addon/assets/css/font-awesome.min.css',
    'parent-style-css': '/wp-content/themes/salient/style.css',
    'salient-wp-menu-dynamic-css': '/wp-content/uploads/salient/menu-dynamic.css',
}


def normalize(nodes, court):
    generators = [n for n in nodes if n['tag']=='meta' and n['attrs'].get('name')=='generator']
    versions = [n for n in generators if re.fullmatch(r'WordPress \d+\.\d+(?:\.\d+)?', str(n['attrs'].get('content','')))]
    if (len(versions)!=1 or not any(str(n['attrs'].get('content','')).startswith('Powered by WPBakery Page Builder -') for n in generators)
            or not any(n['tag']=='link' and 'https://api.w.org/' in n['attrs'].get('rel',[]) for n in nodes)):
        raise ValueError('Unrecognized Circuit 8 WPBakery page')
    metadata, components = [], []

    def tracked(kind, value):
        metadata.append(dict(property=kind,value_sha256=h.sha(value)))

    def component(node,key,kind,location):
        value=node[key]
        components.append(dict(court=court,kind=kind,sha256=h.sha(value),location=location))
        node[key]={'flwu_shared_component':kind}

    # A version/asset URL change needs one same-court review, never automatic stripping.
    component(versions[0]['attrs'],'content','wordpress_release','meta.generator')
    ids={}
    for number,node in enumerate(nodes):
        identifier=node['attrs'].get('id')
        if identifier:
            if not isinstance(identifier,str) or identifier in ids:raise ValueError('Duplicate/unknown DOM ID')
            ids[identifier]=(number,node)
        attrs=node['attrs']
        if node['tag']=='link' and identifier in ASSETS:
            value=attrs.get('href');parsed=urlsplit(value or '')
            if (attrs.get('rel')!=['stylesheet'] or parsed.scheme!='https' or parsed.hostname!=court
                    or parsed.path!=ASSETS[identifier] or parsed.fragment or not re.fullmatch(r'ver=[0-9.]+',parsed.query)):
                raise ValueError('Unknown stylesheet resource')
            component(attrs,'href','wordpress_asset',identifier)
        if node['tag']=='link' and identifier=='redux-google-fonts-salient_redux-css':
            parsed=urlsplit(attrs.get('href',''))
            if attrs.get('rel')!=['stylesheet'] or parsed.scheme!='https' or parsed.netloc!='fonts.googleapis.com' or parsed.path!='/css' or parsed.fragment:
                raise ValueError('Unknown font resource')
            component(attrs,'href','wordpress_asset',identifier)
        if node['tag']=='script' and identifier=='wp-emoji-settings':
            if attrs.get('type')!='application/json' or len(node['children'])!=1:raise ValueError('Unknown emoji configuration')
            data=DECODER.decode(node['children'][0]['value']);value=data['source']['concatemoji'];parsed=urlsplit(value)
            if (parsed.scheme!='https' or parsed.hostname!=court or parsed.path!='/wp-includes/js/wp-emoji-release.min.js'
                    or parsed.fragment or not re.fullmatch(r'ver=[0-9.]+',parsed.query)):
                raise ValueError('Unknown emoji resource')
            component(data['source'],'concatemoji','wordpress_asset','wp-emoji-settings.source.concatemoji')
            node['children'][0]['value']=data
        if node['tag']=='script' and identifier=='nectar-frontend-js-extra':
            if len(node['children'])!=1:raise ValueError('Unknown Nectar localization')
            child=node['children'][0];text=child['value'];match=re.match(r'\s*var nectarLove = ',text)
            if not match:raise ValueError('Unknown Nectar assignment')
            data,end=DECODER.raw_decode(text[match.end():]);token=data.get('loveNonce')
            if not isinstance(token,str) or not re.fullmatch('[0-9a-f]{10}',token):raise ValueError('Unknown Nectar nonce')
            tracked('nectarLove.loveNonce',token);data['loveNonce']={'flwu_tracked_metadata':'nectarLove.loveNonce'}
            # Exact suffix retains nectarOptions and all remaining script logic.
            child['value']=text[:match.end()]+h.canonical(data)+text[match.end()+end:]

    bindings={}
    for identifier,(number,node) in ids.items():
        attrs=node['attrs'];classes=attrs.get('class',[])
        if re.fullmatch('fws_[0-9a-f]{13}',identifier):
            if node['tag']!='div' or not {'wpb_row','vc_row'}<=set(classes):raise ValueError('Unknown row identity')
            bindings[identifier]='FLWU_ROW_'+str(number)
        elif re.fullmatch(r'uvc-exp-wrap-\d{4}-[1-9]\d*',identifier):
            content_id=identifier+'-content';content=ids.get(content_id)
            if (node['tag']!='div' or 'ult_exp_section' not in classes or attrs.get('role')!='button'
                    or attrs.get('aria-controls')!=content_id or attrs.get('data-ultimate-target')!='#'+identifier
                    or not content or content[1]['tag']!='div' or 'ult_exp_content' not in content[1]['attrs'].get('class',[])):
                raise ValueError('Unbound expandable procedure section')
            bindings[identifier]='FLWU_EXPAND_'+str(number)
            bindings[content_id]='FLWU_EXPAND_'+str(number)+'-content'

    # Rewrite only proven declaration/reference fields; an unknown use blocks reuse.
    for node in nodes:
        attrs=node['attrs'];identifier=attrs.get('id')
        if identifier in bindings:
            tracked('wpbakery_dom_id',identifier);attrs['id']=bindings[identifier]
            if attrs.get('aria-controls') in bindings:attrs['aria-controls']=bindings[attrs['aria-controls']]
            target=attrs.get('data-ultimate-target','')
            if target.startswith('#') and target[1:] in bindings:attrs['data-ultimate-target']='#'+bindings[target[1:]]
    remaining=json.dumps(nodes,ensure_ascii=False)
    if bindings and re.search('|'.join(re.escape(x) for x in sorted(bindings,key=len,reverse=True)),remaining):
        raise ValueError('Unknown reference to generated DOM identity')
    return metadata,components
