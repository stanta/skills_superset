"""Offline packaging/routing tests, not payment execution or model evaluation."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / 'atomic-skills' / 'apple-pay-integration'
IDENTIFIER = 'apple-pay-integration'
OWNERS = {'meta-finance-payments', 'meta-mobile-desktop'}


class ApplePaySkillTests(unittest.TestCase):
    def test_portable_frontmatter_and_scope(self):
        body = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(body.startswith('---\nname: apple-pay-integration\ndescription:'))
        self.assertIn('provider-neutral', body)
        self.assertIn('research-only', body)
        self.assertLess(len(body.splitlines()), 220)
        for file in SKILL.rglob('*'):
            if file.is_file():
                text = file.read_text(encoding='utf-8').lower()
                self.assertNotIn('mamanova', text, str(file))
                self.assertNotIn('маманова', text, str(file))
                self.assertNotIn('-----begin private key-----', text, str(file))

    def test_local_markdown_links(self):
        files = list(SKILL.rglob('*.md')) + [ROOT / 'docs/research/apple-pay-integration-practices.md']
        for file in files:
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', file.read_text(encoding='utf-8')):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                path = (file.parent / target.split('#', 1)[0]).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()), (file, target))
                self.assertTrue(path.is_file(), (file, target))

    def test_source_register_and_case_schema(self):
        sources = (SKILL / 'references/sources.md').read_text(encoding='utf-8')
        known = set(re.findall(r'\*\*([APS]\d+) —', sources))
        self.assertGreaterEqual(len(known), 20)
        for file in SKILL.rglob('*.md'):
            for group in re.findall(r'\[((?:[APS]\d+)(?:, [APS]\d+)*)\]', file.read_text(encoding='utf-8')):
                self.assertTrue(set(group.split(', ')) <= known, (file, group))
        data = json.loads((SKILL / 'evals/cases.json').read_text(encoding='utf-8'))
        self.assertEqual(data['status'], 'designed_not_model_benchmarked')
        self.assertGreaterEqual(len(data['cases']), 16)
        self.assertEqual(len({case['id'] for case in data['cases']}), len(data['cases']))
        self.assertEqual({case['kind'] for case in data['cases']}, {'positive', 'negative', 'adversarial'})
        for case in data['cases']:
            self.assertTrue(case['prompt'])
            self.assertTrue(case['must_include'])
            self.assertTrue(case['must_not_include'])
            self.assertTrue(set(case['sources']) <= known)

    def test_meta_membership_and_registry(self):
        memberships = set()
        for file in (ROOT / 'skills').glob('meta-*/references/members.md'):
            text = file.read_text(encoding='utf-8')
            lines = [line for line in text.splitlines() if line.startswith('- **' + IDENTIFIER + '**')]
            if lines:
                self.assertEqual(len(lines), 1)
                self.assertTrue(lines[0].endswith('`../../../atomic-skills/apple-pay-integration/SKILL.md`'))
                memberships.add(file.parent.parent.name)
                count = re.search(r'^(\d+) atomic skills\.', text, re.MULTILINE)
                self.assertIsNotNone(count)
                self.assertEqual(int(count.group(1)), sum(line.startswith('- **') for line in text.splitlines()))
        self.assertEqual(memberships, OWNERS)
        registry = (ROOT / 'skills/meta-specialist-catalog/references/legacy-names.md').read_text(encoding='utf-8')
        lines = [line for line in registry.splitlines() if line.startswith('- **' + IDENTIFIER + '**')]
        self.assertEqual(len(lines), 1)
        self.assertEqual(set(lines[0].split(' — ')[1].split(', ')), OWNERS)

    def test_navigation_and_sensitive_decisions(self):
        for owner in OWNERS:
            self.assertIn('Apple Pay', (ROOT / 'skills' / owner / 'SKILL.md').read_text(encoding='utf-8'))
        for name in ('README.md', 'docs/metaskills.md'):
            self.assertIn('apple-pay-integration/SKILL.md', (ROOT / name).read_text(encoding='utf-8'))
        web = (SKILL / 'references/web-and-native.md').read_text(encoding='utf-8')
        self.assertIn('2026-10-01', web)
        self.assertIn('paymentCredentialStatusUnknown', web)
        self.assertIn('PSP test mode is a separate axis', web)
        backend = (SKILL / 'references/backend-security.md').read_text(encoding='utf-8')
        for term in ('unknown/reconciling', 'SSRF', 'outbox', 'business effect'):
            self.assertIn(term, backend)
        config = (SKILL / 'templates/env.example').read_text(encoding='utf-8')
        self.assertIn('APPLE_PAY_ENABLED=false', config)
        self.assertIn('PSP_API_MODE=test', config)
        self.assertIn('APPLE_PAY_SESSION_ENVIRONMENT=\n', config)


if __name__ == '__main__':
    unittest.main()
