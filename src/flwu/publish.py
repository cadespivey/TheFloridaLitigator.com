"""Validated artifact build and real GitHub Pages workflow generation."""
from pathlib import Path
import json
from flwu.site import build_site


class PublishError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(f'[{code}] {message}')


def build_deployable(archive_dir, output_dir):
    """Build from reviewed public exports, never copy arbitrary private folders."""
    return build_site(archive_dir, Path(output_dir) / 'dist')


def publish_workflow_config(branch='main'):
    return {
        'name': 'GitHub Pages',
        'on': {'push': {'branches': [branch], 'paths': ['website/updates/**', 'website/county-directories/**', 'src/flwu/**', 'pyproject.toml', '.github/workflows/pages.yml']},
               'pull_request': {'paths': ['website/updates/**', 'website/county-directories/**', 'src/flwu/**', 'tests/**', 'pyproject.toml', '.github/workflows/pages.yml']},
               'workflow_dispatch': {}},
        'permissions': {'contents': 'read'},
        'concurrency': {'group': 'pages-${{ github.ref }}', 'cancel-in-progress': False},
        'jobs': {
            'build': {'runs-on': 'ubuntu-latest', 'steps': [
                {'uses': 'actions/checkout@v6'},
                {'uses': 'actions/setup-python@v6', 'with': {'python-version': '3.13'}},
                {'name': 'Install', 'run': 'python -m pip install . pytest'},
                {'name': 'Test', 'run': 'PYTHONDONTWRITEBYTECODE=1 python -m pytest -q'},
                {'name': 'Build reviewed public archive', 'run': 'PYTHONDONTWRITEBYTECODE=1 flwu publish --archive website/updates --output build/site --county-directory website/county-directories/alachua.json --county-directory website/county-directories/bay.json --county-directory website/county-directories/brevard.json --county-directory website/county-directories/broward.json --county-directory website/county-directories/charlotte.json --county-directory website/county-directories/citrus.json --county-directory website/county-directories/collier.json --county-directory website/county-directories/columbia.json --county-directory website/county-directories/duval.json --county-directory website/county-directories/escambia.json --county-directory website/county-directories/flagler.json --county-directory website/county-directories/hendry.json --county-directory website/county-directories/hernando.json --county-directory website/county-directories/highlands.json --county-directory website/county-directories/hillsborough.json --county-directory website/county-directories/indian-river.json --county-directory website/county-directories/levy.json --county-directory website/county-directories/jackson.json --county-directory website/county-directories/lake.json --county-directory website/county-directories/lee.json --county-directory website/county-directories/leon.json --county-directory website/county-directories/manatee.json --county-directory website/county-directories/marion.json --county-directory website/county-directories/martin.json --county-directory website/county-directories/sumter.json --county-directory website/county-directories/suwannee.json --county-directory website/county-directories/gadsden.json --county-directory website/county-directories/okeechobee.json --county-directory website/county-directories/wakulla.json --county-directory website/county-directories/desoto.json --county-directory website/county-directories/baker.json --county-directory website/county-directories/bradford.json --county-directory website/county-directories/washington.json --county-directory website/county-directories/hardee.json --county-directory website/county-directories/taylor.json --county-directory website/county-directories/gilchrist.json --county-directory website/county-directories/holmes.json --county-directory website/county-directories/madison.json --county-directory website/county-directories/dixie.json --county-directory website/county-directories/union.json --county-directory website/county-directories/jefferson.json --county-directory website/county-directories/gulf.json --county-directory website/county-directories/miami-dade.json --county-directory website/county-directories/monroe.json --county-directory website/county-directories/nassau.json --county-directory website/county-directories/okaloosa.json --county-directory website/county-directories/orange.json --county-directory website/county-directories/osceola.json --county-directory website/county-directories/palm-beach.json --county-directory website/county-directories/pasco.json --county-directory website/county-directories/pinellas.json --county-directory website/county-directories/polk.json --county-directory website/county-directories/putnam.json --county-directory website/county-directories/santa-rosa.json --county-directory website/county-directories/sarasota.json --county-directory website/county-directories/seminole.json --county-directory website/county-directories/st-lucie.json --county-directory website/county-directories/volusia.json --county-directory website/county-directories/walton.json'},
                {'uses': 'actions/upload-pages-artifact@v4', 'with': {'path': 'build/site'}},
            ]},
            'deploy': {
                'if': "github.event_name != 'pull_request' && github.ref == 'refs/heads/" + branch + "'",
                'needs': 'build', 'runs-on': 'ubuntu-latest',
                'permissions': {'pages': 'write', 'id-token': 'write'},
                'environment': {'name': 'github-pages', 'url': '${{ steps.deployment.outputs.page_url }}'},
                'steps': [{'uses': 'actions/configure-pages@v5'},
                          {'name': 'Deploy', 'id': 'deployment', 'uses': 'actions/deploy-pages@v4'}],
            },
        },
    }


def write_github_workflow(workflow_dir):
    """JSON is a YAML 1.2 subset and is accepted by GitHub workflow parsing."""
    workflow_dir = Path(workflow_dir)
    workflow_dir.mkdir(parents=True, exist_ok=True)
    path = workflow_dir / 'pages.yml'
    path.write_text(json.dumps(publish_workflow_config(), indent=2) + '\n', encoding='utf-8')
    return path
