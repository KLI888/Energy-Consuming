$(document).ready(function () {
    // Toggle theme
    $('#toggle-theme').click(function () {
        $('body').toggleClass('bg-dark').toggleClass('bg-light');
        $('#toggle-theme').toggleClass('btn-dark').toggleClass('btn-light');
    });

    // Add appliance form submission
    $('#add-appliance-form').submit(function (e) {
        e.preventDefault();
        const appliance = $('#appliance').val();
        const hours = $('#hours').val();
        $.post('/add_appliance', { appliance, hours }, function () {
            location.reload();
        });
    });

    // Predict bill form submission
    $('#predict-form').submit(function (e) {
        e.preventDefault();
        const prev_bill1 = $('#prev_bill1').val();
        const prev_bill2 = $('#prev_bill2').val();
        const prev_bill3 = $('#prev_bill3').val();

        $.post('/predict_bill', { prev_bill1, prev_bill2, prev_bill3 }, function (data) {
            $('#prediction-result').text(`Predicted Bill: ₹${data.predicted_bill.toFixed(2)}`);
        });
    });
});
