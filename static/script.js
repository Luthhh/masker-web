const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

function captureFrame() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');

    fetch('/upload_frame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL })
    })
    .then(res => res.json())
    .then(data => {
        const result = document.getElementById('result');
        result.innerHTML = `<img src="data:image/jpeg;base64,${data.image}" width="640"/>`;
    });
}

setInterval(captureFrame, 1000);

// Tambahkan animasi saat elemen muncul
const sections = document.querySelectorAll('.info-section');

window.addEventListener('scroll', () => {
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            section.classList.add('animate__animated', 'animate__fadeInUp');
        }
    });
});
