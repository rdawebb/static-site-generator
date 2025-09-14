# import the necessary modules
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        self.assertEqual(repr(node), "HTMLNode(div, Hello, children: [], {'class': 'container'})")

    # test props to html with no props
    def test_props_to_html_no_props(self):
        node = HTMLNode("div", "Hello", [], None)
        self.assertEqual(node.props_to_html(), "")

    # test constructor with default values
    def test_constructor_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    # test representation with default values
    def test_repr_defaults(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, children: None, None)")

    # test with no tag
    def test_no_tag(self):
        node = HTMLNode(value="Hello", children=[], props={"class": "container"})
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    # test with no value
    def test_no_value(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    # test with children
    def test_with_children(self):
        child = HTMLNode("span", "Child", [], {"class": "child"})
        node = HTMLNode("div", "Hello", [child], {"class": "container"})
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].value, "Child")

class TestLeafNode(unittest.TestCase):
    # test constructor
    def test_constructor(self):
        node = LeafNode("img", None, {"src": "image.png"})
        self.assertEqual(node.tag, "img")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"src": "image.png"})

    # test leaf to html with img tag
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Click me!", {"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image">Click me!</img>')

    # test leaf to html with no props
    def test_leaf_to_html_no_props(self):
        node = LeafNode("img", "Click me!")
        self.assertEqual(node.to_html(), '<img>Click me!</img>')

    # test leaf to html with no tag
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text") # expect plain text output

    # test leaf to html with no value
    def test_leaf_to_html_no_value(self):
        node = LeafNode("img", None)
        with self.assertRaises(ValueError):
            node.to_html() # expect ValueError

    # test leaf to html with p tag
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

class TestParentNode(unittest.TestCase):
    # test constructor
    def test_constructor(self):
        child = LeafNode("span", "Child", {"class": "child"})
        node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props, {"class": "container"})

    # test parent to html
    def test_parent_to_html(self):
        child = LeafNode("span", "Child", {"class": "child"})
        node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span class="child">Child</span></div>')

    # test parent to html with children
    def test_to_html_with_children(self):
        child = LeafNode("span", "child")
        parent_node = ParentNode("div", [child])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # test parent to html with multiple children
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")

    # test parent to html with grandchildren
    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent_node = ParentNode("div", [child])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # test parent to html with no children
    def test_parent_to_html_no_children(self):
        node = ParentNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html() # expect ValueError

    # test parent to html with another parent as child
    def test_parent_to_html_with_parent_child(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent_node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span><b>grandchild</b></span></div>',
        )

    # test parent to html with no tag
    def test_parent_to_html_no_tag(self):
        child = LeafNode("span", "child")
        node = ParentNode(None, [child], {"class": "container"})
        with self.assertRaises(ValueError):
            node.to_html() # expect ValueError

    # test parent to html with no props
    def test_parent_to_html_no_props(self):
        child = LeafNode("span", "child")
        node = ParentNode("div", [child], None)
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

# run the tests
if __name__ == "__main__":
    unittest.main()