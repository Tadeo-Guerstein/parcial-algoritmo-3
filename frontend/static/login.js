const URL = "http://localhost:8000";
const username = document.getElementById("username");
const form = document.querySelector("form");

async function handleSubmit(event) {
  event.preventDefault();

  const user = username.value;

  const response = await fetch(`${URL}/login`, {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: user }), // Cambiado de 'username' a 'name'
  });

  const { message, error, customerID } = await response.json();
  if (response.status !== 200) {
    alert(error);
    return;
  }

  alert(message);

  localStorage.setItem("customerID", customerID);
  window.location.href = "./customers";
}

form.onsubmit = handleSubmit;
