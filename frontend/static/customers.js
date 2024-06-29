const URL = "http://localhost:8000";
const tableContainer = document.querySelector(".table-responsive");
const tbody = document.querySelector("tbody");
const logout = document.getElementById("logout");

async function getCustomers() {
    const response = await fetch(`${URL}/customers`);
    if (response.status === 200) return await response.json();
}
function isLogged() {
    let flag = true;
    if (!sessionStorage.getItem("customerID")) {
        window.location.href = "/";
        flag = false;
    }
    return flag;
}
async function handleOnLoad() {
    if (!isLogged()) return;
    const { data: customers } = await getCustomers();
    if (customers.length > 0) {
        fillCustomerTable(customers);
        return;
    }
}

function fillCustomerTable(data) {
    data.forEach((i) => {
        const tBodyRow = tbody.insertRow();
        const tBodyCellId = tBodyRow.insertCell();
        const tBodyCellName = tBodyRow.insertCell();
        const tBodyCellGroup = tBodyRow.insertCell();
        const tBodyCellEstado = tBodyRow.insertCell();
        tBodyCellId.innerText = i.id;
        tBodyCellName.innerText = i.nombre;
        tBodyCellGroup.innerText = i.groups?.join?.(", ") || "Orden vacía";
        tBodyCellEstado.innerText = "Activo";
        if (!i.isLogged) {
            tBodyCellEstado.innerText = "Inactivo";
        }
    });
}

async function handleLogout() {
    const customerID = sessionStorage.getItem("customerID");
    const response = await fetch(`${URL}/logout/${customerID}`, {
        method: "PUT",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    sessionStorage.removeItem("customerID");
    response.status === 200 ? (window.location.href = "/") : null;
}

document.onload = handleOnLoad();
logout.addEventListener("click", handleLogout);

let isNavigating = undefined;
window.addEventListener("beforeunload", () => {isNavigating ?? handleLogout();});
window.addEventListener("click", (event) => { if (event.target.tagName === "A" && event.target.href) isNavigating = true; });
window.addEventListener("load", () => { isNavigating = undefined; });