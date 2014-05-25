var re = new RegExp(/SCP-[0-9]+/g);

function add_name(text)
{
    return text + " (herp)";
}

/**
 * Walk function credit
 * http://stackoverflow.com/a/1175866
 */
function walk(node)
{
    node = node || document.body;

    if (node.nodeType == 3) {
        node.nodeValue = node.nodeValue.replace(re, add_name);
    } else {
        var nodes = node.childNodes;
        if (nodes) {
            var i = nodes.length;
            while (i--) walk(nodes[i]);
        }
    }
}

window.onload = walk();
