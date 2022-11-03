const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
      userDataDir: "./user_data", headless:true
});
  const page = await browser.newPage();
  await page.goto('http://localhost:8888/login');
  await browser.close();
})();
