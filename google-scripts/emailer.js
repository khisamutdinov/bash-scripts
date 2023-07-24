/*
|--------------------------------------------------------------------------
| Cleanup Old Emails 
|--------------------------------------------------------------------------
| The script is inspired by https://gist.github.com/benbjurstrom/00cdfdb24e39c59c124e812d5effa39a
|
*/
const INCLUDES = '{category:updates category:promotions category:social} ';
const EXCLUDES = '-in:important -in:starred';
const DELETE_QUERY = INCLUDES + EXCLUDES;
const ARCHIVE_QUERY = 'in:inbox';
// Archive messages after how many days?
const ARCHIVE_AFTER_DAYS = 90;
// Purge messages automatically after how many days?
const DELETE_AFTER_DAYS = 365;

// Maximum number of message threads to process per run. 
const PAGE_SIZE = 200;
// When to run the next batch if the page is exceeded
const NEXT_TRIGGER_IN_MINS = 2;

const DRY_RUN = false;
const CLEAN_ALL = true;
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
 * Create a trigger that executes the doMore{Action} function NEXT_TRIGGER_IN_MINS minutes from now
 */
function setMoreTrigger(action){
  ScriptApp.newTrigger('do' + action)
  .timeBased()
  .at(new Date((new Date()).getTime() + NEXT_TRIGGER_IN_MINS * 60 * 1000))
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
 * Deletes filtered emails from the inbox that are more then DELETE_AFTER_DAYS days old
 */
function doPurge() {
  doAction(DELETE_QUERY, PURGE, DELETE_AFTER_DAYS);
}

/**
 * Archives filtered emails from the inbox that are more then ARCHIVE_AFTER_DAYS days old
 */
function doArchive() {
  doAction(ARCHIVE_QUERY, ARCHIVE, ARCHIVE_AFTER_DAYS);
}

/**
 * @private
 * The actual function that does all the magic
 * Executes an action on filtered emails that are cutoffDays old
 */
function doAction(search, action, cutoffDays) {
  removeMoreTriggers(action);
  const query = `${search} older_than:${cutoffDays}d`;
  console.log(query);
  const threads = GmailApp.search(query, 0, PAGE_SIZE)
  
  if (CLEAN_ALL && threads.length === PAGE_SIZE) {
    console.log(`Reached the PAGE_SIZE=${PAGE_SIZE}. Setting a trigger to call the doMore function in ${NEXT_TRIGGER_IN_MINS} minutes.`);
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
        console.log(`(${i+1}) ${action} [${thread.getLabels().map(l => l.getName()).join(", ")}]: ${thread.getFirstMessageSubject()}`);
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
