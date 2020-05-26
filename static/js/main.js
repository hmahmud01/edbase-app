// Window section hide and load
window.onload = function() {
    // hideContent();
};

// Full Content Hiding Function
function hideContent(){
    var doctor = document.getElementById("doctor");
    var medicine = document.getElementById("medicine");
    doctor.style.display = "none";
    medicine.style.display = "none";
}

// Only Doctor Section Loading Function
function toggleDoctor(){
    var doctor = document.getElementById("doctor");
    var medicine = document.getElementById("medicine");
    // var doctorBack = document.getElementById("doctor-par-back");

    medicine.style.display = "none";
    if(doctor.style.display == "none"){
        doctor.style.display = "block";
        // doctorBack.style.display = "block";
    }else{
        doctor.style.display = "none"
    }
}

// Only Medicine Section Loading Function
function toggleMedicine(){
    var doctor = document.getElementById("doctor");
    var medicine = document.getElementById("medicine");

    doctor.style.display = "none";

    if(medicine.style.display == "none"){
        medicine.style.display = "block";        
    }else{
        medicine.style.display = "none"
    }
}

// Remove All content when going back to the page
function removeToTop(){
    setTimeout(hideContent, 1500);
}