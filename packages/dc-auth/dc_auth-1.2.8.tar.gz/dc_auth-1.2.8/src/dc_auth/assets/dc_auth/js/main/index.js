// import Bulma from '@vizuaalog/bulmajs';

import Alert from '@vizuaalog/bulmajs/src/plugins/Alert';
import Dropdown from '@vizuaalog/bulmajs/src/plugins/Dropdown';
import File from '@vizuaalog/bulmajs/src/plugins/File';
import Message from '@vizuaalog/bulmajs/src/plugins/Message';
import Navbar from '@vizuaalog/bulmajs/src/plugins/Navbar';

/**
 * Roll out our own Tab handling which supports nested tabs
 * Also roll out own own Modal handling
 */

document.addEventListener('DOMContentLoaded', () => {
    /**
     * Iterate over all clickable Tabs and show/hide the content
     * based on the initial state.
     *
     * Then binds a click handler to each tab: => find target,
     * hides all siblings, then shows this target.
     *
     * HTML structure as:
     * <ul class="tabs is-clickable">
     *     <li class="tab is-active"><a href="#one">one</a></li>
     *     <li class="tab"><a href="#two">two</a></li>
     *     <li class="tab"><a href="#three">three</a></li>
     * </ul>
     * <div class="tabs-content">
     *     <div class="tab-content is-active" id="one">one</div>
     *     <div class="tab-content" id="two">two</div>
     *     <div class="tab-content" id="three">three</div>
     * </div>
     * @type {T[]}
     */

        // Note: the $ sign does not mean jQuery! The $ sign is an identifier for variables and functions.
        // it's not a special character (has no significance to the interpreter)

        // Get all "clickable tab" elements

    const t0 = performance.now();

    const $clickableTabs = Array.prototype.slice.call(document.querySelectorAll('.tabs.is-clickable'), 0);

    if ($clickableTabs.length > 0) {

        // Add a click event on each of them
        $clickableTabs.forEach(ct => {

            const $tabList = Array.prototype.slice.call(ct.querySelectorAll('.tab'), 0);

            $tabList.forEach(t => {

                // e.g #overview
                const tabTarget = t.getElementsByTagName('a')[0].getAttribute("href");

                // hide or show this tabs content depending on the current '.is-active' class
                const el = document.getElementById(tabTarget.substring(1));

                // hide or show tab content based on their current is-active state (i.e. on page load)
                const $thisTabContent = Array.prototype.slice.call(el.parentElement.querySelectorAll('.tab-content'))
                updateTabsState($thisTabContent);


                t.addEventListener('click', (e) => {
                    e.preventDefault();

                    // take the is-active class off the other tabs
                    const $tabSiblings = getSiblings(t);
                    $tabSiblings.forEach(tabSibling => {
                        tabSibling.classList.remove("is-active");
                    });
                    t.className += ' is-active ';

                    // update the tab content given this element was clicked
                    const el = document.getElementById(tabTarget.substring(1));

                    // hide all .tab-content
                    const $contentSiblings = getSiblings(el);
                    $contentSiblings.forEach(contentSibling => {
                        contentSibling.style.display = "none";
                        contentSibling.classList.remove("is-active");
                    });

                    // show the targeted element
                    el.style.display = "block";
                    el.className += ' is-active ';
                })
            })

        })
    }

    const t1 = performance.now();
    // console.log("Call to $clickableTabs took " + (t1 - t0) + " milliseconds.")
});

document.addEventListener('DOMContentLoaded', () => {
    /*
     * Toggle modal hide/close using html only
     */

    const openModalButtons = document.getElementsByClassName("open-modal");
    const closeModalButtons = document.getElementsByClassName("close-modal");

    Array.from(openModalButtons).forEach(function (element) {
        element.addEventListener('click', toggleModalClasses);
    });
    Array.from(closeModalButtons).forEach(function (element) {
        element.addEventListener('click', toggleModalClasses);
    });

});
const getSiblings = function (elem) {

    // Setup siblings array and get the first sibling
    const siblings = [];
    let sibling = elem.parentNode.firstChild;

    // Loop through each sibling and push to the array
    while (sibling) {
        if (sibling.nodeType === 1 && sibling !== elem) {
            siblings.push(sibling);
        }
        sibling = sibling.nextSibling
    }

    return siblings;

};

const updateTabsState = function ($tabContent) {
    /**
     * If the tab content panel contains .is-active,
     * display:block, else display:none
     */

    $tabContent.forEach(elem => {

        if (elem.nodeType !== Node.TEXT_NODE) { // ensure we're checking a node not text elem
            const tabContent = elem;
            if (tabContent.classList.contains('tab-content')) {
                if (tabContent.classList.contains('is-active')) {
                    tabContent.style.display = "block";
                } else {
                    tabContent.style.display = "none";
                    tabContent.classList.remove("is-active");
                }
            }
        }

    });

};

function toggleModalClasses(event) {
    /*
    <a class="open-modal" data-modal-id="my-modal">Open My Modal</a>

    <div aria-hidden="" class="modal" id="my-modal">
        <div class="modal-background close-modal" data-modal-id="my-modal"></div>
        <div class="modal-content">
            Content
        </div>
        <button aria-label="close" class="delete close-modal" data-modal-id="my-modal"></button>
    </div>
     */
    const modalId = event.currentTarget.dataset.modalId;
    const modal = document.getElementById(modalId);
    modal.classList.toggle('is-active');
    document.documentElement.classList.toggle('is-clipped');
}


document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    const $notification = $delete.parentNode;
    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
});
