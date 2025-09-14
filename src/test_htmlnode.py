# import the necessary modules
import unittest
from htmlnode import HTMLNode

# define the test case class
class TestHTMLNode(unittest.TestCase):
    # test constructor
    def test_constructor(self):
        node = HTMLNode("div", "Hello", [], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})
    
    # test props to html
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello", [], {"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')
    
    # test representation
    def test_repr(self):
        node = HTMLNode("div", "Hello", [], {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'container'})")

# run the tests
if __name__ == "__main__":
    unittest.main()