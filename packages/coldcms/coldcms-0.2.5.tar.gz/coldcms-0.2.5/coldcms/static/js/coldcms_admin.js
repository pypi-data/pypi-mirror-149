// Event handler for choice blocks with conditional visibility
function onChoiceHandlerChangeBlock(target) {
  const choiceHandler = target.closest('.coldcms-admin__choice-handler');
  if (choiceHandler !== null) {
    let choiceHandlerValue = choiceHandler.querySelector('select').value;

    let searchContainer = choiceHandler.closest('div.struct-block');
    const choiceHandlerIdRegex = /coldcms-admin__choice-handler--([a-zA-Z\-\_\d]+)/;
    const choiceHandlerId = choiceHandlerIdRegex.exec(choiceHandler.className)[1];
    const choiceHandlerTargets = searchContainer.querySelectorAll('.coldcms-admin__choice-handler-target--' + choiceHandlerId);


    for (let j = 0; j < choiceHandlerTargets.length; j++) {
      let matches;
      const hiddenIfRegex = /coldcms-admin__choice-handler-hidden-if--([\w\-]+)/g;
      matches = hiddenIfRegex.exec(choiceHandlerTargets[j].className);
      let choiceHandlerTargetContainer = choiceHandlerTargets[j]
      if(matches){
        let hiddenIfValue = matches[1];
        if (choiceHandlerValue === hiddenIfValue){
          choiceHandlerTargetContainer.parentElement.classList.add('coldcms-admin__choice-handler-target--hidden')
        }else{
          choiceHandlerTargetContainer.parentElement.classList.remove('coldcms-admin__choice-handler-target--hidden')
        }
      }
    }
  }
}

function onChoiceHandlerChangeField(target) {
  const choiceHandler = target.closest('.coldcms-admin__choice-handler');
  if (choiceHandler !== null) {
    let choiceHandlerValue = choiceHandler.querySelector('select').value;

    let searchContainer = choiceHandler.closest('ul.fields');
    const choiceHandlerIdRegex = /coldcms-admin__choice-handler--([a-zA-Z\-\_\d]+)/;
    const choiceHandlerId = choiceHandlerIdRegex.exec(choiceHandler.className)[1];
    const choiceHandlerTargets = searchContainer.querySelectorAll('.coldcms-admin__choice-handler-target--' + choiceHandlerId);

    for (let j = 0; j < choiceHandlerTargets.length; j++) {
      let matches;
      const hiddenIfRegex = /coldcms-admin__choice-handler-hidden-if--([\w\-]+)/g;
      matches = hiddenIfRegex.exec(choiceHandlerTargets[j].className);
      let choiceHandlerTargetContainer = choiceHandlerTargets[j]
      if(matches){
        let hiddenIfValue = matches[1];
        if (choiceHandlerValue === hiddenIfValue){
          choiceHandlerTargetContainer.classList.add('coldcms-admin__choice-handler-target--hidden')
        }else{
          choiceHandlerTargetContainer.classList.remove('coldcms-admin__choice-handler-target--hidden')
        }
      }
    }
  }
}



// Initialize a collapsible panel
function initCollapsablePanel(panelHeader) {
  panelHeader.addEventListener('click', function() {
    if (this.parentElement.classList.contains('coldcms-admin__panel--collapsed')) {
      this.parentElement.classList.remove('coldcms-admin__panel--collapsed');
    } else {
      this.parentElement.classList.add('coldcms-admin__panel--collapsed');
    }
  });
}

// Initialize a collapsable struct block
function initCollapsableStructBlock(structBlockContainer, collapsed = false) {
  if(structBlockContainer.querySelector('.collapse-button') == null){
    structBlockContainer.insertAdjacentHTML(
      'afterbegin',
      `<button class="c-sf-block__actions__single disabled collapse-button" type="button" title="Collapse">
      <i class="icon icon-view collapse-icon" aria-hidden="true"></i>
      <i class="icon icon-no-view collapse-icon-hidden" aria-hidden="true"></i>
      </button>`
    )
  }
  let collapseButton = structBlockContainer.querySelector('.collapse-button')
  if(collapsed){
    structBlockContainer.parentElement.classList.add('coldcms-admin__struct-block--collapsed');
  }
  collapseButton.addEventListener('click', function(event) {
    if (collapseButton.parentElement.parentElement.classList.contains('coldcms-admin__struct-block--collapsed')) {
      collapseButton.parentElement.parentElement.classList.remove('coldcms-admin__struct-block--collapsed');
      collapseButton.querySelector('.icon-no-view').classList.remove('collapse-icon-hidden')
      collapseButton.querySelector('.icon-view').classList.add('collapse-icon-hidden')
    } else {
      collapseButton.parentElement.parentElement.classList.add('coldcms-admin__struct-block--collapsed');
      collapseButton.querySelector('.icon-view').classList.remove('collapse-icon-hidden')
      collapseButton.querySelector('.icon-no-view').classList.add('collapse-icon-hidden')
    }
  });

}

// Initialize a choice handler
function initChoiceHandlerBlock(structBlockContainer) {
  structBlockContainer.addEventListener('change', function(event) {
    onChoiceHandlerChangeBlock(event.target);
  });
}

function initChoiceHandlerField(structBlockContainer) {
  structBlockContainer.addEventListener('change', function(event) {
    onChoiceHandlerChangeField(event.target);
  });
}

// Event handler for when a new struct block is created
var callback_watcher = function(mutationsList) {
    let k;
    let l;
    let choiceHandlerSelects;
    for (let j = 0; j < mutationsList.length; j++) {
      for (k = 0; k < mutationsList[j].addedNodes.length; k++) {
        // Make sure the choice handler is run for each new choice block
        let node = mutationsList[j].addedNodes[k]
        const structBlockContainers = node.querySelectorAll('.c-sf-block > .c-sf-block__header');
        for (i = 0; i < structBlockContainers.length; i++) {
          initCollapsableStructBlock(structBlockContainers[i]);
        }
        const structBlockFields = node.querySelectorAll('.c-sf-block > .c-sf-block__content > .c-sf-block__content-inner > .struct-block > .field > .c-sf-container > div');
        for (i = 0; i < structBlockFields.length; i++) {
          initWatcher(structBlockFields[i]);
        }
        const streamBlockFields = node.querySelectorAll('.c-sf-block > .c-sf-block__content > .c-sf-block__content-inner > .c-sf-container > div');
        for (i = 0; i < streamBlockFields.length; i++) {
          initWatcher(streamBlockFields[i]);
        }

        const choiceHandlersCharFieldSelects = document.querySelectorAll('.coldcms-admin__choice-handler > .field-content > .input > select');
        for (i = 0; i < choiceHandlersCharFieldSelects.length; i++) {
          initChoiceHandlerBlock(choiceHandlersCharFieldSelects[i]);
          onChoiceHandlerChangeBlock(choiceHandlersCharFieldSelects[i]);
        }
      }
    }
};


function initWatcher(panelFields) {
  const observer = new MutationObserver(callback_watcher);
  observer.observe(panelFields, {
    attributes: false,
    childList: true,
    subtree: false,
  });
}

// Initialize all event handlers on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize collapsable panels
    let i;
    const panelHeaders = document.querySelectorAll('.object:not(.collapsible) > .title-wrapper');
    for (i = 0; i < panelHeaders.length; i++) {
      initCollapsablePanel(panelHeaders[i]);
    }

    const panelFields = document.querySelector('#content_blocks-list');
    if(panelFields){
      initWatcher(panelFields);
    }

    // Initialize stream field related features
    let observer;
    const structBlockContainers = document.querySelectorAll('.c-sf-block > .c-sf-block__header');
    for (i = 0; i < structBlockContainers.length; i++) {
      initCollapsableStructBlock(structBlockContainers[i], true);
    }

    const structBlockFields = document.querySelectorAll('.c-sf-block > .c-sf-block__content > .c-sf-block__content-inner > .struct-block > .field > .c-sf-container > div');
    for (i = 0; i < structBlockFields.length; i++) {
      initWatcher(structBlockFields[i]);
    }

    // Initialize choice handler for selectboxes not contained in stream fields
    const choiceHandlersCharFieldSelectsBlock = document.querySelectorAll('.coldcms-admin__choice-handler > .field-content > .input > select');
    for (i = 0; i < choiceHandlersCharFieldSelectsBlock.length; i++) {
      initChoiceHandlerBlock(choiceHandlersCharFieldSelectsBlock[i]);
      onChoiceHandlerChangeBlock(choiceHandlersCharFieldSelectsBlock[i]);
    }

    const choiceHandlersCharFieldSelectsField = document.querySelectorAll('.coldcms-admin__choice-handler > .field > .field-content > .input > select');
    for (i = 0; i < choiceHandlersCharFieldSelectsField.length; i++) {
      initChoiceHandlerField(choiceHandlersCharFieldSelectsField[i]);
      onChoiceHandlerChangeField(choiceHandlersCharFieldSelectsField[i]);
    }
});
