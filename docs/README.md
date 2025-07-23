# Welcome to the StaffNet project documentation!

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## How to run the project

1. Access the dev server `172.16.0.115` via SSH
2. Go to the project directory `cd /var/www/StaffNet/`
3. Run the following command to start the frontend server: `npm run dev`
4. The frontend server will start running on port 3000 that is to say, you can access the frontend by going to `http://172.16.0.115:3000`
5. The frontend server will automatically update when changes are made to the code
6. To stop the frontend server, press `Ctrl + C`

## How to add new options to the input fields

1. Go to the file `./src/assets/arrayData.js`
2. Identify the input field you want to add options to, for example, the `cargo` input field
3. Add the new options to the `cargo` array, for example:

```javascript
...
{
    id: "cargo",
    label: "Cargo",
    name: "cargo",
    type: "select",
    options: [
        // another options
        { value: "NEW OPTION", label: "New Option" }
    ],
},
...
```
> **Note:** The `value` property is the value that will be sent to the backend in uppercase and the `label` property is the value that will be displayed to the user

> **Note:** If the input is about a campaign, you should add the new option to the `campana_general` array and to the `gerencia` array as well

## How to deploy a new version of the project to the production server

1. Build the project by running the following command: `npm run build`
2. Use the following command to copy the build folder to the production server: `scp -r dist/ ares@172.16.0.114:/var/www/StaffNet/`
3. Access the production server `172.16.0.114` via SSH
4. Restart the host server by running the following command: `sudo systemctl reload apache2`


