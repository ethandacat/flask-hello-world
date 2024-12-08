// ==UserScript==
// @name         Discourse Extras
// @namespace    ethandacatProductions
// @version      1.1
// @description  More for viewing, less for writing.
// @author       ethandacat
// @match        https://x-camp.discourse.group/*
// @icon         https://d3bpeqsaub0i6y.cloudfront.net/user_avatar/meta.discourse.org/discourse/48/148734_2.png
// @grant        none
// ==/UserScript==

function descCode(element) {
    while (element) {
        if (element.tagName && element.tagName.toLowerCase() === 'code') {
            return true;
        }
        element = element.parentElement;
    }
    return false;
}

function gText(element) {
    const avoid = /<*>/
    const regex = /!\{(.*?)\}/g; // Match !{stuff} normally
    const matches = [];
    const input = element.innerHTML;
    // Replace !{stuff} with an empty string and store the matches
    const cleanedText = input.replace(regex, (match, p1) => {
        var mna;
        const ql = p1.split(" ");
        const cmd = ql[0];
        const arg = ql[1];
        const argt = ql.slice(2).join(" ");
        switch (cmd) {
            case "phantom":
                mna = "";
                break;
            case "bgc":
                mna = `<span style="background-color:${arg}">`;
                break;
            case "color":
                mna = `<span style="color:${arg}">`;
                break;
            case "style":
                mna = `<span style="${arg} ${argt}">`;
                break;
            case "s":
                mna = "</span>";
                break;
            case "size":
                mna = `<span style="font-size:${arg}px;">`;
                break;
            case "codepen":
                mna = `<iframe src="https://cdpn.io/${arg}/fullpage/${argt}?view=" frameborder="0" width="90%" height="600px" style="clip-path: inset(120px 0 0 0); margin-top: -120px;"></iframe>`;
                break;
            case "embed":
                var pw = `${arg} ${argt}`.replace("<a href=\"","");
                mna = `<iframe style="width:900px;height:600px;" src="${pw}" frameborder="0"></iframe>`;
                break;
            default:
                mna = "<span style='color:red; background-color:yellow; padding:1px; margin:1px; border: 1px solid red; '>Invalid Discourse Extras Tag!</span>";
                break;

        }
        return mna; // Remove the matched pattern
    });

    return cleanedText.trim();
}

// Function to process .cooked elements
function processCookedElement(element) {
    const result = gText(element); // Get cleaned text and extracted content
    element.innerHTML = result; // Update the element's innerHTML
}

// Create a MutationObserver to watch for added nodes
const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
            // Check if the added node is an element
            if (node.nodeType === Node.ELEMENT_NODE) {
                // If it's a .cooked element, process it
                if (node.classList.contains('cooked')) {
                    processCookedElement(node);
                }
                // If the added node has children, check them for .cooked elements
                node.querySelectorAll('.cooked').forEach(cookedElement => {
                    processCookedElement(cookedElement);
                });
            }
            // Check if the added node is an element
            if (node.nodeType === Node.ELEMENT_NODE) {
                // If it's a .cooked element, process it
                if (node.classList.contains('chat-message-text')) {
                    processCookedElement(node);
                }
                // If the added node has children, check them for .cooked elements
                node.querySelectorAll('.chat-message-text').forEach(cookedElement => {
                    processCookedElement(cookedElement);
                });
            }
        });
    });
});

// Start observing the document for changes
observer.observe(document.body, {
    childList: true, // Observe direct children
    subtree: true // Observe all descendants
});

// Initial processing of existing .cooked elements
document.querySelectorAll('.cooked').forEach(processCookedElement);

