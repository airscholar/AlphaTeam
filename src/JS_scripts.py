"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: JS_scripts module contains script to insert into the plotly graph for dynamic functionality
"""

# ----------------------------------------- SCRIPTS ----------------------------------------- #


scripts = {
    'to_clipboard_no_map': '<script type="text/javascript">const graph = document.getElementsByClassName("xy");graph['
                           '0].addEventListener("click",function() {const hoverlayer = '
                           'document.getElementsByClassName("hoverlayer");const data =hoverlayer[0].innerHTML;const '
                           'text = data.substring(data.indexOf(">Node: ")+7, data.indexOf("</text>"));console.log('
                           'text);copyToClipboard(text);});function copyToClipboard(text) {var dummy = '
                           'document.createElement("textarea");document.body.appendChild(dummy);dummy.value = '
                           'text;dummy.select();document.execCommand("copy");document.body.removeChild('
                           'dummy);}</script>',
    'to_clipboard_map': '<script type="text/javascript">const graph=document.getElementsByClassName("layer bg");const '
                        'rect=graph[0].getElementsByTagName("rect");const observer=new MutationObserver(function(e){'
                        'e.forEach(function(e){if(e.attributeName!=="class"){if(e.target.style.cursor!=="pointer"){'
                        'return};const hoverlayer=document.getElementsByClassName("hoverlayer");const '
                        'data=hoverlayer[0].innerHTML;const text=data.substring(data.indexOf(">Node: ")+7,'
                        'data.indexOf("</text>"));copyToClipboard(text);console.log(text)}})});observer.observe(rect['
                        '0],{attributes:!0});function copyToClipboard(t){var e=document.createElement('
                        '"textarea");document.body.appendChild(e);e.value=t;e.select();document.execCommand('
                        '"copy");document.body.removeChild(e)};</script>',
}
