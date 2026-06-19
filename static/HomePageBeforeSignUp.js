// Initialize AOS
AOS.init({
    duration: 800,
    once: true,
});

// --- Mobile Menu Toggle ---
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

mobileMenuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});


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

function animate() {
    requestAnimationFrame(animate);
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