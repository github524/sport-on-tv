const output = document.getElementById("output");

const today = new Date().toLocaleDateString(undefined, {
  weekday: "long",
  month: "long",
  day: "numeric"
});

output.innerHTML = `
  <strong>${today}</strong><br><br>
  No data source connected yet.
`;
