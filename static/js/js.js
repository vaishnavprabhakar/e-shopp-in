$(".remove-cart").click(function () {
  console.log("hello");
  var id = $(this).attr("pid").toString();
  var eml = this;
  console.log("pid =", id);

  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log("data =", data);
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
      eml.parentNode.parentNode.parentNode.parentNode.remove();
       console.log("data =" ,data)
       eml.innerText = data.quantity
       document.getElementById("amount").innerHTML=data.amount
       document.getElementById("totalamount").innerText=data.totalamount
       eml.parentNode.parentNode.parentNode.parentNode.remove()
    },
  });
});

$(".plus-cart").click(function () {
  console.log("plus button");
  var id = $(this).attr("pid").toString();

  var eml = this;
  console.log(eml);
  console.log("pid =", id);

  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log("data =", data);
      document.getElementById("quantity").innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });

  
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this;
  console.log("pid =", id);
  console.log(eml.parentNode.children[2]);
  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log("data =", data);
      document.getElementById("quantity").innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});






// google pay payment gateway






