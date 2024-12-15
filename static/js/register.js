const usernameField = document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const FeedbackArea = document.querySelector(".feedbackArea");
const emailFeedbackArea = document.querySelector(".emailfeedbackArea")
const usernamesuccessOutput = document.querySelector(".usernamesuccessOutput");
const emailsuccessOutput = document.querySelector(".emailsuccessOutput");
const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");
const ValidatesubmitBtn = document.querySelector("#usernameField, #emailField, #passwordField")
/* work on ValidatesubmitBtn */




showPasswordToggle.addEventListener("click", (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE"
        passwordField.setAttribute("type", "text")
    }
    else {
    showPasswordToggle.textContent = "SHOW"
    passwordField.setAttribute("type", "password")
    }
})


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    console.log("usernameVal", usernameVal);

    usernamesuccessOutput.style.display = "block";
    usernamesuccessOutput.textContent = `checking ${usernameVal}...`;

 
    usernameField.classList.remove("is-invalid");
    FeedbackArea.style.display = "none";

    if (usernameVal.length > 0){
        fetch('/authentication/validate-username',{
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            console.log("data", data);
            usernamesuccessOutput.style.display = "none";
            if (data.username_error){
                usernameField.classList.add("is-invalid");
                FeedbackArea.style.display = "block";
                FeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;
            }else {
                submitBtn.removeAttribute("disbled")
            }
            
            
        });
        
    }


});


emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    console.log("emailVal", emailVal);

    emailsuccessOutput.style.display = "block";
    emailsuccessOutput.textContent = `checking ${emailVal}...`;

    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display = "none";

    if (emailVal.length > 0){
        fetch('/authentication/validate-email',{
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            console.log("data", data);
            if (data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                submitBtn.disbled = true;
            }else {
                submitBtn.removeAttribute("disbled")
            }
        });
        
    }


});

