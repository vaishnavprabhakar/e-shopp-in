

$('.btn-heart').click(function(){
  console.log('Wishlist');
  var id = $(this).attr("pid").toString();
  console.log(id);
  // console.log($(this));
  alert('working')
  $.ajax({
  type : "GET",
  url  : "/wishlist",
  data : {
    prod_id : id,
  },

  success:function(data){
    console.log('Success');
    window.location.href = `http://localhost:7000/${id}`
  },
  })
})



$(".remove-cart").click(function () {
  console.log("hello");
  var id = $(this).attr("pid").toString();
  var eml = $(this.parentNode.parentNode);
  console.log("pid =", id);
  console.log("eml =", eml);
  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log('success fucntion',data);
      if (data.refresh) {
        location.reload();
      }  else{
      console.log("data =", data);
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
      eml.remove();
      }
    },
  });
});




$(".plus-cart").click(function () {
  console.log("plus button");
  var id = $(this).attr("pid").toString();
  var qty = document.getElementById("quantity")
  // var eml = $(this.parentNode.parentNode.children[1]);
  console.log('eml=',qty);
  console.log("pid =", id);

  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },

    success: function (data) {   

        // eml.innerText = data.quantity;
        qty.value = data.quantity;
        console.log("data =", data.quantity);
        document.getElementById('amount').innerText = data.amount;
        document.getElementById('totalamount').innerText = data.totalamount;
    },
  });
  
});



$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  // var eml = $(this.parentNode.parentNode.children[1]);
  var qty = document.getElementById("quantity")
  console.log("pid =", id);
  console.log('eml =', qty);
  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log("data =", data);
      // eml.innerText = data.quantity;
      qty.value = data.quantity;
      document.getElementById('amount').innerText = data.amount;
      document.getElementById('totalamount').innerText = data.totalamount;
    },
  });
});





