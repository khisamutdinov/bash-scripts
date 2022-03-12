/*
|--------------------------------------------------------------------------
| Cleanup Old Emails 
|--------------------------------------------------------------------------
| The script is inspired by https://gist.github.com/benbjurstrom/00cdfdb24e39c59c124e812d5effa39a
|
*/
const DRY_RUN = false;
// Maximum number of message threads to process per run. 
const PAGE_SIZE = 200;

const ARCHIVE = 'Archive';
const PURGE = 'Purge';

/**
 * Create a trigger that executes the clenup function every day.
 * Execute this function to install the script.
 */
function setCleanupTrigger() {
  ScriptApp
    .newTrigger('cleanup')
    .timeBased()
    .everyDays(1)
    .create()
}

/**
 * Create a trigger that executes the doMore{Action} function two minutes from now
 */
function setMoreTrigger(action){
  ScriptApp.newTrigger('do' + action)
  .timeBased()
  .at(new Date((new Date()).getTime() + 1000 * 60 * 2))
  .create()
}

/**
 * Deletes all triggers that call the doMore{Action} function.
 */
function removeMoreTriggers(action){
  var triggers = ScriptApp.getProjectTriggers()
  for (var i = 0; i < triggers.length; i++) {
    var trigger = triggers[i]
    if(trigger.getHandlerFunction() === 'do' + action){
      ScriptApp.deleteTrigger(trigger)
    }
  }
}

/**
 * Deletes all of the project's triggers
 * Execute this function to unintstall the script.
 */
function removeAllTriggers() {
  var triggers = ScriptApp.getProjectTriggers()
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i])
  }
}

/**
 * Wrapper for the start all actions
 */
function cleanup() {
  doPurge();
  doArchive();
}

/**
 * Deletes filtered emails from the inbox that are more then 365 days old
 */
function doPurge() {
  const EXCLUDES = '-in:important -in:starred ';
  const INCLUDES = '{category:updates category:promotions category:social} ';
  // Purge messages automatically after how many days?
  const DELETE_AFTER_DAYS = 365;
  const search = EXCLUDES + INCLUDES;
  doAction(search, PURGE, DELETE_AFTER_DAYS);
}

/**
 * Archives filtered emails from the inbox that are more then 90 days old
 */
function doArchive() {
  const ARCHIVE_AFTER_DAYS = 90;
  const search = 'in:inbox';
  doAction(search, ARCHIVE, ARCHIVE_AFTER_DAYS);
}

/**
 * @private
 * The actual function that does all the magic
 * Executes an action on filtered emails that are cutoffDays old
 */
function doAction(search, action, cutoffDays) {
  removeMoreTriggers(action);
  const query = search + ' older_than:' + cutoffDays + 'd';
  console.log(query);
  const threads = GmailApp.search(query, 0, PAGE_SIZE)
  
  if (threads.length === PAGE_SIZE) {
    console.log('PAGE_SIZE exceeded. Setting a trigger to call the doMore function in N minutes.');
    setMoreTrigger(action);
  }
  
  console.log('Processing ' + threads.length + ' threads...');
  
  // The date to start execute an action
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - cutoffDays);
  
  // For each thread matching our search
  try {
    for (let i = 0; i < threads.length; i++) {
      const thread = threads[i];
      
      // Only act if the newest message in the thread is older then DELETE_AFTER_DAYS
      if (thread.getLastMessageDate() < cutoff) {
        console.log('(' + i + ') ' + action + 'ing [' + thread.getLabels().join(", ") + ']: '  + thread.getFirstMessageSubject());
        if(!DRY_RUN) {
          switch(action) {
            case PURGE: {
              thread.moveToTrash();
              break;
            }
            case ARCHIVE : {
              thread.moveToArchive();
              break;
            }
            default : {
              console.log('Action is not specified');
            }
          }
          
        }
      }
    }
  } catch(e) {
    console.error(e);
    removeMoreTriggers(action);
    throw e;
  }
}