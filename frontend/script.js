const API = "http://127.0.0.1:8000";

let editId = null;   // track editing contact

window.onload = getContacts;


// get all
async function getContacts() {
    const res = await fetch(`${API}/contacts`);
    const data = await res.json();
    renderTable(data);
}


// create OR update
async function createContact() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;

    // UPDATE MODE
    if (editId !== null) {
        await fetch(`${API}/contacts/${editId}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, phone })
        });

        editId = null;
        document.querySelector("button[onclick='createContact()']").innerText = "Save";
    }
    // CREATE MODE
    else {
        await fetch(`${API}/contacts`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, phone })
        });
    }

    clearInputs();
    getContacts();
}


// fill form for editing
function editContact(contact) {
    editId = contact.id;

    document.getElementById("name").value = contact.name;
    document.getElementById("email").value = contact.email;
    document.getElementById("phone").value = contact.phone;

    document.querySelector("button[onclick='createContact()']").innerText = "Update";
}


// delete
async function deleteContact(id) {
    await fetch(`${API}/contacts/${id}`, { method: "DELETE" });
    getContacts();
}


// search
async function searchContact() {
    const name = document.getElementById("searchName").value;
    const res = await fetch(`${API}/contacts/search?name=${name}`);
    const data = await res.json();
    renderTable(data);
}


// render
function renderTable(data) {
    const tbody = document.querySelector("#contactsTable tbody");
    tbody.innerHTML = "";

    data.forEach(c => {
        const row = `
            <tr>
                <td>${c.id}</td>
                <td>${c.name}</td>
                <td>${c.email}</td>
                <td>${c.phone}</td>
                <td>
                    <button onclick='editContact(${JSON.stringify(c)})'>Edit</button>
                    <button onclick="deleteContact(${c.id})">Delete</button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}


// helper
function clearInputs() {
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("phone").value = "";
}
