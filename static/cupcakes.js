URL_API = 'http://127.0.0.1:5000/api'
DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"
const ul = document.getElementById('list-cupcakes');

$(document).ready(showInitialCupcakes());

function liCupcake(cupcake){
    
    const newLi = document.createElement("li");
    newLi.innerHTML = `${cupcake['flavor']} / ${cupcake['size']} / ${cupcake['rating']}`;
    newLi.className = 'list-group-item d-flex justify-content-between align-items-center';

    const xButton = document.createElement('button');
    xButton.innerHTML = 'X';
    xButton.className = 'delete-cupcake btn-sm btn-danger';
    xButton.setAttribute('data-id', `${cupcake['id']}`);

    const editButton = document.createElement('button');
    editButton.innerHTML = 'E';
    editButton.className = 'edit-cupcake btn-sm btn-primary';
    editButton.setAttribute('data-id', `${cupcake['id']}`);
    
    newLi.appendChild(xButton);
    newLi.appendChild(editButton);
    ul.appendChild(newLi);
}

async function showInitialCupcakes() {
    const resp = await axios.get(`${URL_API}/cupcakes`);
    for (let key in resp.data.cupcakes){
        liCupcake(resp.data.cupcakes[key]);
    }
} 

$("#list-cupcakes").on("click", ".delete-cupcake", deleteCupcake);

async function deleteCupcake() {
    const id = $(this).data('id');
    await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().remove();
}

$("#list-cupcakes").on("click", ".edit-cupcake", showEditCupcake);

async function showEditCupcake() {
    const id = $(this).data('id');
    const resp = await axios.get(`${URL_API}/cupcakes/${id}`);
    cupcake = resp.data.cupcake;
    $("#flavor").val(cupcake['flavor']);
    $("#rating").val(cupcake['rating']);
    $("#size").val(cupcake['size']);
    $("#image").val(cupcake['image']);
    
    $("#patch-cupcake").removeClass("hidden");
    $("#add-cupcake").addClass("hidden");

    $("#patch-cupcake").attr('data-id',`${cupcake['id']}`);

}

$("form").on("click", "#patch-cupcake", patchCupcake);

async function patchCupcake(event) {
    const id = $(this).data('id');
    event.preventDefault();

    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();
    if(image == ""){
        image = DEFAULT_IMAGE;
    }

    CUPCAKE_DATA = {
        "flavor": flavor, "size": size,
        "rating": rating, "image": image
    }
    
    const resp = await axios.patch(`${URL_API}/cupcakes/${id}`, json=CUPCAKE_DATA)
    console.log(resp)

    $("form").trigger("reset");

}



/** handle form for adding of new cupcakes */

$("form").on("click", "#add-cupcake", addCupcake);

async function addCupcake(event) {
    event.preventDefault();
  
    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    if(image == ""){
        image = DEFAULT_IMAGE;
    }
  
    const resp = await axios.post(`${URL_API}/cupcakes`, 
            { flavor, rating, size, image});
  
    liCupcake(resp.data.cupcake);

    $("form").trigger("reset");

}