document.querySelectorAll(".carousel").forEach(carousel => {

        const images = carousel.querySelectorAll("img")
        let index = 0

        carousel.querySelector(".next").onclick = () => {
            images[index].style.display = "none"
            index = (index + 1) % images.length
            images[index].style.display = "block"
        }

        carousel.querySelector(".prev").onclick = () => {
            images[index].style.display = "none"
            index = (index - 1 + images.length) % images.length
            images[index].style.display = "block"
        }

    })