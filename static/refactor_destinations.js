const fs = require('fs');
const path = require('path');

const excludeFiles = [
    'homepage.html', 'index.html', 'login.html', 'Front.html', 
    'mapping3.html', 'todolist.html', 'scrapbook.html', 'pr.html'
];

const dir = process.cwd();
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !excludeFiles.includes(f));

const templateTop = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery - Traveloop</title>
    <link rel="stylesheet" href="global.css">
    <style>
        body {
            padding-top: 100px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .gallery-container {
            width: 90%;
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
        }
        .pa-gallery-player-widget {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <nav class="navbar animate-up">
        <div class="nav-logo">
            <a href="homepage.html">Traveloop</a>
        </div>
        <div class="nav-links">
            <a href="homepage.html" class="nav-item">Home</a>
            <a href="mapping3.html" class="nav-item">Map</a>
            <a href="todolist.html" class="nav-item">To-Do list</a>
            <a href="pr.html" class="nav-item">Chat Bot</a>
            <a href="scrapbook.html" class="nav-item">Snaps</a>
        </div>
    </nav>

    <div class="gallery-container glass-card animate-up delay-1">
        <h2 class="section-title text-gradient" style="text-align: center; text-transform: capitalize;">DESTINATION_NAME</h2>
`;

const templateBottom = `
    </div>
</body>
</html>`;

files.forEach(file => {
    let content = fs.readFileSync(path.join(dir, file), 'utf8');
    
    // Extract everything between <script src="https://cdn.jsdelivr.net/npm/publicalbum@latest/embed-ui.min.js" async></script> and </body>
    const scriptTag = '<script src="https://cdn.jsdelivr.net/npm/publicalbum@latest/embed-ui.min.js" async></script>';
    const startIndex = content.indexOf(scriptTag);
    let galleryContent = "";
    
    if (startIndex !== -1) {
        const bodyEndIndex = content.indexOf('</body>');
        if (bodyEndIndex !== -1) {
            galleryContent = content.substring(startIndex, bodyEndIndex).trim();
        } else {
            galleryContent = content.substring(startIndex).replace('</html>', '').trim();
        }
    } else {
        console.log("Could not find gallery in " + file);
        return;
    }

    const destinationName = file.replace('.html', '');
    const finalTop = templateTop.replace('DESTINATION_NAME', destinationName);
    
    const newContent = finalTop + '\n        ' + galleryContent + '\n' + templateBottom;
    fs.writeFileSync(path.join(dir, file), newContent);
    console.log("Updated " + file);
});
