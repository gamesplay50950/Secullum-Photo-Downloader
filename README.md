# Secullum-Photo-Downloader

Download photos used for facial recognition in Secullum Web Point easily.
This tool allows you to download photos from the Secullum Ponto Web system to import them or register them in any other system.

# Usage Methods

- If you have a list of employee IDs (that is, a list of the last digits of the employee's URL), you can import it into the system for automatic download.
  
> Ideal if you have an accurate list of employees.

- Use a time interval to download the photos.
  
> If you don't have the IDs or have a large number of employees, this might work well.

# How to use?

The script needs information from your logged-in user's cookies to access the website and download the photos. The script needs the following information:

```
- Authorization
- User-Agent
- Referer
- Cookies
- Employee registration URL (if you don't know it, use URL_EMPLOYEE)
- URL of the location where the photos are stored (if you don't know it, use URL_BIO)
```

- Run the code and enter the data mentioned above (if you don't know where to find it, in the employee's record open the browser's inspect menu, go to the Network tab and reload the page, click on any file in the list and look for the data mentioned).

- After entering the data, provide the URLs. Below is the standard used by Secullum, which you can also use:
  
  - For URL_EMPLOYEE the default is "https://pontoweb.secullum.com.br/Funcionarios/{id}"
    
  - For URL_BIO the default is "https://pontoweb.secullum.com.br/FuncionariosBiometrias/{id}"
    
    > Keep the text "{id}" in the end of the URL to the script works!
    
- Choose between option 1 or 2. Option 1 uses a CSV file to download the photos. If you don't have the files, use option 2, which uses a specific interval to download the photos.
  
  - If you choose option 1, please provide the other requested information about the CSV file.
    
Wait for the process to finish and use the photos as you wish!
