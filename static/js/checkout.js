$(document).ready(function(){
    $('#rzp-button1').click(function(e){
        e.preventDefault();

        var fname = $("[name='sofname']").val();
        var lname = $("[name='solname']").val();
        var email = $("[name='semail']").val();
        var phone = $("[name='sphone']").val();
        var address = $("[name='sadrs']").val();
        var city = $("[name='scity']").val();
        var district = $("[name='sdistrict']").val();
        var pincode = $("[name='spincode']").val();
        var add_message = $("[name='add_det']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        console.log("Form data:", fname, lname, email, phone, address, city, district, pincode, add_message);

        if(fname == "" || lname == "" || email == "" || phone == "" || address == "" || city == "" || district == ""  || pincode == "" || add_message == ""){
            swal("Alert!", "All fields are mandatory", "error");
            return false;
        } else {
            $.ajax({
                method : "GET",
                url: "/proceed-to-pay",
                success: function(response){
                    console.log("Response from proceed-to-pay:", response);
                    var options = {
                        "key": "rzp_test_Ub6QFBei8ww2Pg",
                        "amount": response.total_price * 100,
                        "currency": "INR",
                        "name": "Ecart", //your business name
                        "description": "Thankyou for buying",
                        "image": "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/e-cart-design-template-0850ac300cfc66e069124f37ae291dea_screen.jpg?ts=1635403878",
                        "handler": function (responseb){
                            console.log("Payment response:", responseb);
                            data = {
                                'so_fname' : fname,
                                'so_lname' : lname,
                                'so_email' : email,
                                'so_phone' : phone,
                                'so_address' : address,
                                'so_city' : city,
                                'so_state' : state,
                                'so_district' : district
                                'so_pincode' : pincode,
                                'add_message' : add_message
                                'payment_mode' : 'Razorpay',
                                'payment_id' : responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token
                            };
                            console.log("Data before sending to place-order:", data);
                            $.ajax({
                                method: 'POST',
                                url: '/place-order',
                                data: data,
                                success : function(responsec){
                                    console.log("Response from place-order:", responsec);
                                    swal("Congratulations", responsec.status, "success").then((value) => {
                                        window.location.href = '/myorder';
                                    });
                                },
                                error: function(err){
                                    console.log("Error in place-order AJAX call:", err);
                                }
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": fname+' '+lname, //your customer's name
                            "email": email,
                            "contact": phone  //Provide the customer's phone number for better conversion rates
                             },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                },
                error: function(err){
                    console.log("Error in proceed-to-pay AJAX call:", err);
                }
            });
        }
    });
});