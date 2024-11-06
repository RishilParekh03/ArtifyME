document.addEventListener("DOMContentLoaded", function () {
    const imageUpload = document.getElementById("imageUpload");
    const imagePreview = document.getElementById("imagePreview");
    const convertButton = document.getElementById("convertButton");
    const resetButton = document.getElementById("resetButton");
    const resetButton2 = document.getElementById("resetButton2");
    const actionButtons = document.getElementById("actionButtons");
    const resultButtons = document.getElementById("resultButtons");
    const downloadButton = document.getElementById("downloadButton");
    const flashMsg = document.getElementById('flash_msg');
    const loaderContainer = document.getElementById('loaderContainer');

    imageUpload.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.onload = function () {
                    imagePreview.innerHTML = "";
                    imagePreview.appendChild(img);
                    convertButton.disabled = false;
                };
            };
            reader.readAsDataURL(file);
        }
    });

    convertButton.addEventListener("click", function (e) {
        e.preventDefault();

        loaderContainer.style.display = 'flex';

        const formData = new FormData();
        formData.append('inputImage', imageUpload.files[0]);

        fetch('/converting_image', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {

                loaderContainer.style.display = 'none';

                if (data.processed_image) {
                    const cartoonImage = new Image();
                    cartoonImage.src = data.processed_image;
                    cartoonImage.onload = function () {
                        imagePreview.innerHTML = "";
                        imagePreview.appendChild(cartoonImage);
                        flashMsg.innerHTML = data.message;
                        flashMsg.style.color = 'forestgreen';
                        actionButtons.style.display = "none";
                        resultButtons.style.display = "block";
                        downloadButton.href = data.processed_image;
                    };
                } else {
                    document.getElementById('flash_msg').innerHTML = data.error
                }
            })
            .catch(error => {
                console.error('Error:', error);
                loaderContainer.style.display = 'none';
                document.getElementById('flash_msg').innerHTML = "Something went wrong :("
            });
    });

    function resetPage() {
        imageUpload.value = "";
        imagePreview.innerHTML = "<p>No image uploaded yet</p>";
        actionButtons.style.display = "block";
        resultButtons.style.display = "none";
        convertButton.disabled = true;
    }

    resetButton.addEventListener("click", resetPage);
    resetButton2.addEventListener("click", resetPage);
});
