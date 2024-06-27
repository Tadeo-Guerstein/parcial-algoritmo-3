const URL = "http://localhost:8000";
const tableContainer = document.querySelector(".table-responsive");
const emptyText = document.getElementById("empty-text");
const tbody = document.querySelector("tbody");
const logout = document.getElementById("logout");

async function getUsers() {
  const response = await fetch(`${URL}/users`);
  if (response.status === 200) {
    return await response.json();
  }
}

async function getGrupos() {
  const response = await fetch(`${URL}/groups`);
  if (response.status === 200) {
    return await response.json();
  }
}

async function handleOnLoad() {
  // const { data: users } = await getUsers()
  // const { data: grupos } = await getGrupos()
  // if (grupos.length > 0) {
  //   grupos.forEach((i) => {
  //     const option = document.createElement('option')
  //     option.value = JSON.stringify(i)
  //     option.text = i.name.toUpperCase()
  //     select.add(option)
  //   })
  // }
  // if (users.length > 0) {
  //   users.forEach((i) => {
  //     const tBodyRow = tbody.insertRow()
  //     const tBodyCellId = tBodyRow.insertCell()
  //     const tBodyCellName = tBodyRow.insertCell()
  //     const tBodyCellGroup = tBodyRow.insertCell()
  //     const tBodyCellEstado = tBodyRow.insertCell()
  //     tBodyCellId.innerText = i.id
  //     tBodyCellName.innerText = i.username
  //     tBodyCellGroup.innerText = i.groups?.join?.(', ') || 'Sin grupo'
  //     tBodyCellEstado.innerText = 'Activo'
  //     if (!i.isLogged) {
  //       tBodyCellEstado.innerText = 'Inactivo'
  //     }
  //   })
  //   return
  // }
  // const span = document.createElement('span')
  // span.id = 'empty-text'
  // span.innerText = 'No hay datos para listar'
  // tableContainer.appendChild(span)
}

async function handleOnClickLogout() {
  const customerID = localStorage.getItem("customerID");
  const response = await fetch(`${URL}/logout/${customerID}`, {
    method: "PUT",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
  });
  const data = await response.json();

  if (response.status !== 200) {
    alert(data.error);
    return;
  }

  window.location.href = "/";
}

document.onload = handleOnLoad();
logout.onclick = handleOnClickLogout;
