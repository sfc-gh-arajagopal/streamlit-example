import unittest

from therapy_maps import MAPS, to_markdown, to_mermaid, to_svg


class TherapyMapTests(unittest.TestCase):
    def test_maps_are_complete_and_unique(self):
        ids = [mind_map["id"] for mind_map in MAPS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(MAPS), 8)
        for mind_map in MAPS:
            self.assertTrue(mind_map["title"].strip())
            self.assertTrue(mind_map["summary"].strip())
            self.assertGreaterEqual(len(mind_map["branches"]), 6)
            for branch in mind_map["branches"]:
                self.assertTrue(branch["title"].strip())
                self.assertGreaterEqual(len(branch["items"]), 2)
                self.assertTrue(branch["color"].startswith("#"))

    def test_exports_include_every_node(self):
        for mind_map in MAPS:
            markdown = to_markdown(mind_map)
            mermaid = to_mermaid(mind_map)
            svg, width, height = to_svg(mind_map)
            self.assertIn(mind_map["title"], markdown)
            self.assertIn(mind_map["center"], mermaid)
            self.assertIn(mind_map["center"], svg)
            self.assertGreater(width, 400)
            self.assertGreater(height, 200)
            self.assertTrue(svg.startswith("<svg"))
            self.assertIn("</svg>", svg)
            for branch in mind_map["branches"]:
                self.assertIn(branch["title"], markdown)
                self.assertIn(branch["title"], svg)
                for item in branch["items"]:
                    self.assertIn(item, markdown)
                    self.assertIn(item, svg)


if __name__ == "__main__":
    unittest.main()
