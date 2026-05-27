export const generateProgram = function (server, target, format, config, program, name, callback) {
    const url = new URL(`api/generate/${target}/${format}/`, server);
    url.searchParams.set('name', name);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url.href);
    const formData = new FormData();
    const file = new Blob([program], { type: 'text/plain' });
    formData.append("program", file);
    const configfile = new Blob([JSON.stringify(config)], { type: 'application/json' });;
    formData.append("config", configfile);
    xhr.send(formData);
    xhr.onload = () => {
        if (xhr.readyState == 4) {
            const data = JSON.parse(xhr.response);
            callback(data);
        }
    };
}

export const downloadProgram = function (server, target, format, config, program, name, callback) {
    const url = new URL(`api/download/${target}/${format}/`, server);
    url.searchParams.set('name', name);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url.href);
    const formData = new FormData();
    const file = new Blob([program], { type: 'text/plain' });
    formData.append("program", file);
    const configfile = new Blob([JSON.stringify(config)], { type: 'application/json' });;
    formData.append("config", configfile);
    xhr.send(formData);
    xhr.onload = () => {
        if (xhr.readyState == 4) {
            callback(xhr.response);
        }
    };
}

export const saveFile = function (content, filename) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

export const basename = function (filename) {
    return filename.substring(0, filename.indexOf('.'));
}