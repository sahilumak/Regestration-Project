document.addEventListener("DOMContentLoaded", () => {
    const bugdebuddyBtn = document.getElementById("bugdebuddy-btn");
    const sidePanel = document.getElementById("side-panel");
    const closeBtn = document.getElementById("close-btn");

    // Open the side panel
    bugdebuddyBtn.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent default anchor behavior
        sidePanel.classList.add("active");
    });

    // Close the side panel
    closeBtn.addEventListener("click", () => {
        sidePanel.classList.remove("active");
    });
});

// function Theam(currentTheme) {
//     let currentTheme = 'White';
//     if (currentTheme === "White") {
//         document.body.style.background = "Black";
//         document.body.style.color = "White"; // Optional: Change text color for visibility
//         currentTheme = 'Black'

//     } else {
//         document.body.style.background = "White";
//         document.body.style.color = "Black"; // Optional: Revert text color
//         currentTheme = 'White'
//     }
// }

// // Attach the event listener to the button
// document.getElementById('Theame').onclick = Theam;
    // Call the function with the desired the

document.getElementById('dark').onclick=dark1;
document.getElementById('light').onclick=light1;
function dark1(){
    document.body.style.background='Black'
    document.body.style.color='White'
}
function light1(){
    document.body.style.background='White'
    document.body.style.color='Black'
    
}
const header = document.getElementById('header');
const content = document.querySelector('.content');
const headerHeight = header.offsetHeight;
content.style.marginTop = `${headerHeight}px`;


