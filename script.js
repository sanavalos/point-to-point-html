document.getElementById("customer").onclick = function() {myFunction("customer")};
document.getElementById("pointer").onclick = function() {myFunction("pointer")};

let customerBullets = ["Browse through the available products, add items to their cart, and complete the purchase online. They can also filter and search for products based on their preferences and needs.", "Select their preferred pickup location from a list of available options, allowing them to collect their purchased items conveniently. They can even change the pickup location if needed before finalizing the order.", "Access their order history to review past purchases, track orders, and check the status of their pickups. This helps them keep a record of their transactions and easily reorder their favorite products.", "Leave feedback and ratings for products and sellers, helping to build trust within the online marketplace community. Their feedback contributes to the overall reputation of sellers and assists other shoppers in making informed decisions."]
let pointerBullets = ["Create product listings, including descriptions, prices, and availability, making their items visible to potential customers. They can also set promotions or discounts to attract more buyers.", "Track and manage their inventory, updating product availability and stock levels in real-time. This ensures that customers always see accurate information about product availability.", "Receive and fulfill customer orders, preparing products for pickup at the chosen location. They can update order status, mark items as ready for pickup, and communicate with customers about the pickup process.", "Communicate with customers through the platform, addressing inquiries, resolving issues, and providing assistance throughout the buying process. They can also use the messaging system to inform customers about order updates or promotions."]

function myFunction(user) {
 let bullets = document.getElementsByClassName("actions");
 if (user == "customer") {
  bullets[0].innerHTML = "";
  document.getElementById("customer").classList.add("selected-user");
  document.getElementById("pointer").classList.remove("selected-user");
  for (let i = 0; i < customerBullets.length; i++) {
   let li = document.createElement("li");
   li.innerText = customerBullets[i];
   bullets[0].appendChild(li);
  }
 } 
 if (user == "pointer") {
  bullets[0].innerHTML = "";
  document.getElementById("pointer").classList.add("selected-user");
  document.getElementById("customer").classList.remove("selected-user");
  for (let i = 0; i < pointerBullets.length; i++) {
   let li = document.createElement("li");
   li.innerText = pointerBullets[i];
   bullets[0].appendChild(li);
  }
 }
}
myFunction('customer')

const actions = document.getElementsByClassName("actions");
