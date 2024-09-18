function fetchLogEntries() {
    fetch('/log_entries')
        .then(response => response.json())
        .then(data => {
            const logContainer = document.querySelector('.container');

            data.entries.forEach(entry => {
                const logEntryDiv = document.createElement('div');
                logEntryDiv.classList.add('log-entry');
                logEntryDiv.innerHTML = `<p>${entry}</p>`;
                logContainer.appendChild(logEntryDiv);
            });
        })
        .catch(error => console.error('Error fetching log entries:', error));
  }
  setInterval(fetchLogEntries, 15000);
  fetchLogEntries();
