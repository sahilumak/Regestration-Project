function loadNamePieChart() {
    const namePieChart = document.getElementById('namePieChart');
    const nameHeading = document.getElementById('nameHeading');
    namePieChart.src = '/plot/name_pie';
    namePieChart.style.display = 'block';
    nameHeading.style.display = 'block';
}

function loadDescriptionPieChart() {
    const descriptionPieChart = document.getElementById('descriptionPieChart');
    const descriptionHeading = document.getElementById('descriptionHeading');
    descriptionPieChart.src = '/plot/description_pie';
    descriptionPieChart.style.display = 'block';
    descriptionHeading.style.display = 'block';
}
