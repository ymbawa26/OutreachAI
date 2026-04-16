const SAMPLE_ROWS = [
  {
    Name: "Bruno",
    Email: "bvega@bates.edu",
    Class: "Advanced Software Engineering",
    "Recent Grade": "A",
    "Personal Note": "led the codebase design seamlessly and built an amazing Streamlit integration",
  },
  {
    Name: "Yazan",
    Email: "yazanbawaqna@gmail.com",
    Class: "Intro to AI",
    "Recent Grade": "B+",
    "Personal Note": "did great on the neural network project but missed the last lecture",
  },
];

const requiredColumns = ["Name", "Email", "Class", "Recent Grade", "Personal Note"];

const subjectInput = document.getElementById("subject-input");
const templateInput = document.getElementById("template-input");
const csvUpload = document.getElementById("csv-upload");
const loadSampleButton = document.getElementById("load-sample");
const generateButton = document.getElementById("generate-button");
const downloadButton = document.getElementById("download-button");
const tableWrapper = document.getElementById("table-wrapper");
const tableBody = document.getElementById("table-body");
const dataState = document.getElementById("data-state");
const statusMessage = document.getElementById("status-message");
const resultsState = document.getElementById("results-state");
const resultsList = document.getElementById("results-list");

let rows = [];
let generatedRows = [];

function setStatus(message) {
  statusMessage.textContent = message;
}

function escapeCsvValue(value) {
  const stringValue = String(value ?? "");
  if (stringValue.includes(",") || stringValue.includes("\"") || stringValue.includes("\n")) {
    return `"${stringValue.replace(/"/g, "\"\"")}"`;
  }
  return stringValue;
}

function parseCsv(text) {
  const normalized = text.trim().replace(/\r\n/g, "\n");
  const lines = normalized.split("\n").filter(Boolean);

  if (lines.length < 2) {
    throw new Error("The uploaded CSV needs a header row and at least one data row.");
  }

  const headers = lines[0].split(",").map((header) => header.trim());

  for (const column of requiredColumns) {
    if (!headers.includes(column)) {
      throw new Error(`Missing required column: ${column}`);
    }
  }

  return lines.slice(1).map((line) => {
    const values = line.split(",").map((value) => value.trim());
    return headers.reduce((record, header, index) => {
      record[header] = values[index] ?? "";
      return record;
    }, {});
  });
}

function renderTable() {
  if (!rows.length) {
    tableWrapper.classList.add("hidden");
    dataState.classList.remove("hidden");
    generateButton.disabled = true;
    return;
  }

  tableBody.innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td>${row.Name}</td>
          <td>${row.Email}</td>
          <td>${row.Class}</td>
          <td>${row["Recent Grade"]}</td>
          <td>${row["Personal Note"]}</td>
        </tr>
      `
    )
    .join("");

  dataState.classList.add("hidden");
  tableWrapper.classList.remove("hidden");
  generateButton.disabled = false;
}

function mockAiGenerate(row, baseTemplate) {
  const personalizedGreeting = `Hi ${row.Name},\n\nI hope you're having a good week!`;
  let contextBuilder = `I'm reaching out regarding your progress in ${row.Class}. I saw that your recent grade is a ${row["Recent Grade"]}. `;

  if (row["Recent Grade"].includes("A")) {
    contextBuilder += `Fantastic job! I specifically noticed that you ${row["Personal Note"]}.`;
  } else if (row["Recent Grade"].includes("B")) {
    contextBuilder += `You're doing well! I wanted to mention that you ${row["Personal Note"]}.`;
  } else {
    contextBuilder += `Don't get discouraged! I know you are ${row["Personal Note"]}.`;
  }

  return `${personalizedGreeting}\n\n${contextBuilder}\n\n${baseTemplate}`;
}

function renderResults() {
  if (!generatedRows.length) {
    resultsList.classList.add("hidden");
    resultsState.classList.remove("hidden");
    downloadButton.disabled = true;
    return;
  }

  resultsList.innerHTML = generatedRows
    .map(
      (row, index) => `
        <article class="result-card">
          <div class="result-header">
            <div class="result-title">
              <h3>${row.Name}</h3>
              <p>${row.Email} · ${row.Class}</p>
            </div>
            <label class="checkbox">
              <input type="checkbox" data-index="${index}" checked />
              Keep draft
            </label>
          </div>
          <pre class="draft-text">${row.Generated_Email}</pre>
        </article>
      `
    )
    .join("");

  resultsState.classList.add("hidden");
  resultsList.classList.remove("hidden");
  downloadButton.disabled = false;

  resultsList.querySelectorAll("input[type='checkbox']").forEach((checkbox) => {
    checkbox.addEventListener("change", (event) => {
      const index = Number(event.target.dataset.index);
      generatedRows[index].selected = event.target.checked;
    });
  });
}

function loadRows(newRows, sourceLabel) {
  rows = newRows;
  generatedRows = [];
  renderTable();
  renderResults();
  setStatus(`Loaded ${rows.length} row${rows.length === 1 ? "" : "s"} from ${sourceLabel}.`);
}

function downloadSelectedRows() {
  const selectedRows = generatedRows.filter((row) => row.selected);

  if (!selectedRows.length) {
    setStatus("No drafts are selected for download yet.");
    return;
  }

  const headers = ["Select", ...requiredColumns, "Generated_Email"];
  const csv = [
    headers.join(","),
    ...selectedRows.map((row) =>
      [
        "TRUE",
        row.Name,
        row.Email,
        row.Class,
        row["Recent Grade"],
        row["Personal Note"],
        row.Generated_Email,
      ]
        .map(escapeCsvValue)
        .join(",")
    ),
  ].join("\n");

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "outreachai-generated-emails.csv";
  link.click();
  URL.revokeObjectURL(url);
}

loadSampleButton.addEventListener("click", () => {
  loadRows(SAMPLE_ROWS, "the built-in sample");
});

csvUpload.addEventListener("change", async (event) => {
  const [file] = event.target.files;
  if (!file) {
    return;
  }

  try {
    const text = await file.text();
    const parsedRows = parseCsv(text);
    loadRows(parsedRows, file.name);
  } catch (error) {
    rows = [];
    renderTable();
    setStatus(error.message);
  }
});

generateButton.addEventListener("click", () => {
  const baseTemplate = templateInput.value.trim();

  if (!rows.length) {
    setStatus("Load the sample data or upload a CSV first.");
    return;
  }

  if (!baseTemplate) {
    setStatus("Add a main message before generating drafts.");
    return;
  }

  generatedRows = rows.map((row) => ({
    ...row,
    Subject: subjectInput.value.trim(),
    Generated_Email: mockAiGenerate(row, baseTemplate),
    selected: true,
  }));

  renderResults();
  setStatus(`Generated ${generatedRows.length} personalized draft${generatedRows.length === 1 ? "" : "s"} in browser demo mode.`);
});

downloadButton.addEventListener("click", downloadSelectedRows);
