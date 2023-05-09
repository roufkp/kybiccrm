const tables = document.querySelectorAll('.generated-table');
const rowsPerPage = 10;

tables.forEach((table) => {
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');
  const rowCount = rows.length;
  const pageCount = Math.ceil(rowCount / rowsPerPage);
  const pagination = table.nextElementSibling;

  // Add pagination links
  for (let i = 1; i <= pageCount; i++) {
    const link = document.createElement('a');
    link.href = '#';
    link.innerHTML = i;
    link.addEventListener('click', function(e) {
      e.preventDefault();
      // Set the active link
      const activeLink = pagination.querySelector('.active');
      if (activeLink) {
        activeLink.classList.remove('active');
      }
      link.classList.add('active');
      // Show the rows for the selected page
      const startIndex = (i - 1) * rowsPerPage;
      const endIndex = startIndex + rowsPerPage;
      for (let j = 0; j < rowCount; j++) {
        rows[j].style.display = (j >= startIndex && j < endIndex) ? '' : 'none';
      }
    });
    pagination.appendChild(link);
  }

  // Show the first page by default
  pagination.querySelector('a').classList.add('active');
  for (let i = rowsPerPage; i < rowCount; i++) {
    rows[i].style.display = 'none';
  }
});


//search option

function searchTable(table, input) {
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');
  const searchValue = input.value.trim().toLowerCase();
  const matchingRows = [];

  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll('td');
    const firstCell = cells[0].textContent.trim().toLowerCase();

    if (firstCell.includes(searchValue)) {
      matchingRows.push(rows[i]);
    }
  }

  // Sort the matching rows by the first column in ascending order
  matchingRows.sort((a, b) => {
    const aText = a.querySelector('td').textContent.trim().toLowerCase();
    const bText = b.querySelector('td').textContent.trim().toLowerCase();
    if (aText < bText) return -1;
    if (aText > bText) return 1;
    return 0;
  });

  tbody.innerHTML = '';
  if (matchingRows.length > 0) {
    for (let i = 0; i < matchingRows.length; i++) {
      tbody.appendChild(matchingRows[i]);
    }
  } else {
    const noResultsRow = document.createElement('tr');
    const noResultsCell = document.createElement('td');
    noResultsCell.colSpan = 2;
    noResultsCell.textContent = 'No results found';
    noResultsRow.appendChild(noResultsCell);
    tbody.appendChild(noResultsRow);
  }
}
