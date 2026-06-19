console.log("NEW SCRIPT LOADED");

// Initialize AOS
AOS.init({
    duration: 800,
    once: true,
});

// --- Mobile Menu Toggle ---
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
}

// --- Three.js 3D Background Animation ---
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#hero-canvas'),
    alpha: true
});

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(5);

let mouseX = 0;
let mouseY = 0;

const geometries = [
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.CylinderGeometry(0.5, 0.5, 1.5, 32),
    new THREE.ConeGeometry(0.7, 1.5, 32),
    new THREE.TorusGeometry(0.5, 0.2, 16, 100)
];
const material = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    metalness: 0.6,
    roughness: 0.4,
    transparent: true,
    opacity: 0.2
});

const shapes = [];
for (let i = 0; i < 100; i++) {
    const randomGeometry = geometries[Math.floor(Math.random() * geometries.length)];
    const mesh = new THREE.Mesh(randomGeometry, material);
    const [x, y, z] = Array(3).fill().map(() => THREE.MathUtils.randFloatSpread(100));
    mesh.position.set(x, y, z);
    const [rx, ry, rz] = Array(3).fill().map(() => THREE.MathUtils.randFloat(0, Math.PI * 2));
    mesh.rotation.set(rx, ry, rz);
    const scale = THREE.MathUtils.randFloat(0.3, 0.6);
    mesh.scale.set(scale, scale, scale);
    scene.add(mesh);
    shapes.push(mesh);
}

const pointLight = new THREE.PointLight(0xffffff, 0.1);
pointLight.position.set(5, 5, 5);
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(pointLight, ambientLight);

function onDocumentMouseMove(event) {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
}
document.addEventListener('mousemove', onDocumentMouseMove, false);

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', onWindowResize, false);

let animationId = null;

function animate() {
    animationId = requestAnimationFrame(animate);
    const targetX = mouseX * 3;
    const targetY = mouseY * 3;
    camera.position.x += (targetX - camera.position.x) * 0.05;
    camera.position.y += (targetY - camera.position.y) * 0.05;
    camera.lookAt(scene.position);
    shapes.forEach(shape => {
        shape.rotation.x += 0.001;
        shape.rotation.y += 0.001;
    });
    renderer.render(scene, camera);
}
animate();

// ======================================================
// Resume Upload API Lifecycle
// ======================================================
const resumeInput = document.getElementById("resume-upload");

if (!resumeInput) {
    console.error("Resume upload input not found!");
} else {
    resumeInput.addEventListener("change", uploadResume);
}

async function uploadResume(e) {
    const file = e.target.files[0];

    if (!file) {
        alert("Please select a resume.");
        return;
    }

    console.log("Uploading:", file.name);

    const formData = new FormData();
    formData.append("resume", file);

    // Reset layout text states
    document.getElementById("salary-result").textContent = "Analyzing...";
    document.getElementById("skills-container").innerHTML = "";
    document.getElementById("feedback-container").innerHTML = "";
    document.getElementById("jobs-container").innerHTML = "";
    document.getElementById("resume-score").textContent = "...";

    // Hide redirection button instantly while system is tracking logic
    const exploreBtn = document.getElementById("explore-jobs-btn");
    if (exploreBtn) {
        exploreBtn.classList.add("hidden");
    }

    try {
        console.log("Before fetch");
        const response = await fetch("http://127.0.0.1:5000/upload-resume", {
            method: "POST",
            body: formData
        });

        console.log("After fetch", response);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server returned ${response.status}: ${errorText}`);
        }

        const data = await response.json();
        console.log("Response JSON:", data);
        updateDashboard(data);

    } catch (e) {
        console.log("ERROR NAME:", e.name);
        console.log("ERROR MESSAGE:", e.message);
        document.getElementById("salary-result").textContent = "Upload Failed";
    }
}

function updateDashboard(data) {
    console.log("Updating Dashboard Matrix");

    // Render Salary
    document.getElementById("salary-result").textContent = data.salary || "N/A";

    // Render Resume Score
    document.getElementById("resume-score").textContent = (data.resume_score ?? 0) + "%";

    // Render Skills Badges
    const skillsContainer = document.getElementById("skills-container");
    skillsContainer.innerHTML = "";
    if (Array.isArray(data.skills)) {
        data.skills.forEach(skill => {
            const span = document.createElement("span");
            span.className = "bg-indigo-500 text-white px-3 py-1 rounded-full";
            span.textContent = skill;
            skillsContainer.appendChild(span);
        });
    }

    // Render Feedback Loops
    const feedbackContainer = document.getElementById("feedback-container");
    feedbackContainer.innerHTML = "";
    if (Array.isArray(data.feedback) && data.feedback.length > 0) {
        data.feedback.forEach(item => {
            const div = document.createElement("div");
            div.className = "bg-yellow-500/20 p-3 rounded mt-2";
            div.textContent = item;
            feedbackContainer.appendChild(div);
        });
    } else {
        feedbackContainer.innerHTML = `<div class="text-green-400 font-semibold">Excellent Resume!</div>`;
    }

    // Render Top 5 Machine Learning Job Matches
    const jobsContainer = document.getElementById("jobs-container");
    jobsContainer.innerHTML = "";

    if (Array.isArray(data.job_matches)) {
        data.job_matches.forEach(job => {
            const card = document.createElement("div");
            card.className = "bg-gray-700 p-4 rounded-lg flex justify-between items-center transition-all duration-300 hover:bg-gray-600";
            card.innerHTML = `
                <div>
                    <h5 class="font-bold">${job.title}</h5>
                    <p class="text-sm text-gray-400">${job.company}</p>
                </div>
                <span class="text-green-400 font-bold">${job.match}% Match</span>
            `;
            jobsContainer.appendChild(card);
        });
    }

    // Transition button into view once execution yields matches
    const exploreBtn = document.getElementById("explore-jobs-btn");
    if (exploreBtn && data.job_matches && data.job_matches.length > 0) {
        exploreBtn.classList.remove("hidden");
    }

    // ======================================================
    // NEW CONTENT: AUTOMATIC SMOOTH SCROLL TO DASHBOARD SECTION
    // ======================================================
    const resultsSection = document.getElementById("results");
    if (resultsSection) {
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 300); // Small 300ms delay to allow content to finish drawing on screen smoothly
    }
}

// Smooth scroll actions for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (!targetId || targetId === "#") {
            e.preventDefault();
            return;
        }
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

if (window.innerWidth < 768) {
    renderer.setPixelRatio(1);
}

document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        cancelAnimationFrame(animationId);
    } else {
        animate();
    }
});