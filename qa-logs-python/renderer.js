// Credit: Andy Jackson
// https://github.com/ukwa/webrender-puppeteer

// 'use strict' not required for modules?;

const puppeteer = require('puppeteer');
const PuppeteerHar = require('./puppeteer-har');
const devices = require('puppeteer/DeviceDescriptors');
const fs = require('fs');
const { promisify } = require('util');
const crypto = require('crypto');

const seed = process.argv[2];

process.on('unhandledRejection', error => {
  // Will print "unhandledRejection err is not defined"
  console.log('unhandledRejection: ', error.message);
  process.exit(1);
});

(async () => {

  // Set up the browser in the required configuration:
  const browserArgs = {
    ignoreHTTPSErrors: true,
    args: ['--disk-cache-size=0', '--no-sandbox', '--ignore-certificate-errors'],
  };
  // Add proxy configuration if supplied:
  if (process.env.HTTP_PROXY) {
    browserArgs.args.push('--proxy-server=' + process.env.HTTP_PROXY);
  }
  console.log("Browser arguments: ", browserArgs);
  const browser = await puppeteer.launch(browserArgs);
  const page = await browser.newPage();

  // Set the page size:
  await page.setViewport({ width: 1280, height: 1024 });
  
  // Set the default timeout:
  await page.setDefaultNavigationTimeout( 60000 ); // 60 seconds instead of 30

  // Set the user agent up:
  // Add optional userAgent override:
  if( 'USER_AGENT' in process.env ) {
    page.setUserAgent( process.env['USER_AGENT']);
    // e.g. 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
  } else if( 'USER_AGENT_ADDITIONAL' in process.env ) {
    const user_agent = await browser.userAgent();
    page.setUserAgent( user_agent + " " + process.env['USER_AGENT_ADDITIONAL'] );
  }

  // Set up the additional headers:
  headers = {}
  // Add Memento Datetime header if needed:
  // e.g. Accept-Datetime: Thu, 31 May 2007 20:35:00 GMT
  if( 'MEMENTO_ACCEPT_DATETIME' in process.env ) {
      headers['Accept-Datetime'] = process.env['MEMENTO_ACCEPT_DATETIME']
  }
  // Add a warc-prefix as JSON in a Warcprox-Meta: header
  if( 'WARCPROX_WARC_PREFIX' in process.env ) {
      headers['Warcprox-Meta'] = '{ "warc-prefix": "'+process.env['WARCPROX_WARC_PREFIX']+'" }';
  }
  // Add to page:
  await page.setExtraHTTPHeaders(headers);

  // Record requests/responses in a standard format:
  const har = new PuppeteerHar(page);
  await har.start();

  // Go the the page to capture:
  // See https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md#pagegotourl-options for definitions of networkidle0/2
  console.log("Navigating to " + seed);
  try {
    await page.goto(seed, { waitUntil: 'networkidle2' }); // Longer timeout set above

    // Switch to different user agent settings to attempt to ensure additional media downloaded:
    console.log("Switching device settings...");
    await page.emulate(devices['iPhone 6']);
    await page.emulate(devices['iPhone X landscape']);
    await page.emulate(devices['Nexus 6']);
    
    // Switch through a few widths to encourage JS-based responsive image loading:
    await page.setViewport({ width: 480, height: 1024, deviceScaleFactor: 1, isMobile: false, hasTouch: false, isLandscape: false});
    await page.setViewport({ width: 640, height: 1024, deviceScaleFactor: 1, isMobile: false, hasTouch: false, isLandscape: false});
    await page.setViewport({ width: 800, height: 1024, deviceScaleFactor: 1, isMobile: false, hasTouch: false, isLandscape: false});
    await page.setViewport({ width: 1024, height: 1024, deviceScaleFactor: 1, isMobile: false, hasTouch: false, isLandscape: false});

    // Switch back to the standard device view:
    await page.setViewport({ width: 1280, height: 1024, deviceScaleFactor: 1, isMobile: false, hasTouch: false, isLandscape: false});

    // Scroll down:
    console.log("Scrolling down...");
    await autoScroll(page);

  } catch(e) {
    console.error(e);
    console.log("But lets continue and render what we got.");
  }

  // Look for any "I Accept" buttons
  console.log("Looking for any modal buttons...");
  await clickKnownModals(page);

  // Await for any more elements scrolling down prompted:
  console.log("Waiting for any activity to die down...");
  //await page.waitForNavigation({ waitUntil: 'networkidle0' }); // This will usually hang as this event has already passed.
  await page.waitFor(5000);

  // Render the result:
  console.log("Rendering...");

  // A place to record URLs of different kinds:
  const urls = {};
  // Get the main frame URL:
  urls.url = await page.url();
  // Also get hold of the transcluded resources that make up the page:
  // (this works like capturing page.on('response') events but excludes the URL of the page itself.)
  // urls.E = await page.evaluate(() => (
  //   performance.getEntries()
  //     .filter(e => e.entryType === 'resource')
  //     .map(e => e.name)
  // ));
  // Get hold of the navigation links:
  // urls.L = await page.$$eval('a', as => as.map(a => a.href));
  // urls.L = [...new Set(urls.L)];

  // Get the location of clickable <a> elements:
  // urls.map = await page.evaluate(() => {
  //   const clickables = [];
  //   const elements = Array.prototype.slice.call(document.getElementsByTagName('*'));
  //   elements.forEach((element) => {
  //     if (element.offsetParent != null) {
  //       if (element.onclick != null || element.href !== undefined) {
  //         const c = {};
  //         const {
  //           x, y, width, height,
  //         } = element.getBoundingClientRect();
  //         c.location = {
  //           left: x, top: y, width, height,
  //         };
  //         if (element.attributes.href !== undefined) {
  //           // Get absolute URL:
  //           c.href = element.href;
  //         }
  //         if (element.onclick != null) {
  //           c.onclick = element.onclick.toString();
  //         }
  //         clickables.push(c);
  //       }
  //     }
  //   });
  //   return clickables;
  // });

  // Write out a link summary:
  // await promisify(fs.writeFile)('/output/rendered.urls.json', JSON.stringify(urls));

  // Assemble the HAR:
  const har_standard = await har.stop();
  var har_extended = har_standard;
  har_extended['log']['pages'][0]['url'] = await page.url();
  har_extended['log']['pages'][0]['urls'] = urls;
  // har_extended['log']['pages'][0]['map'] = urls.map;
  // const b64_content = Buffer.from(html).toString('base64');
  // har_extended['log']['pages'][0]['renderedContent'] = { 
  //   text: b64_content, 
  //   encoding: "base64"
  // };
  // const b64_image = Buffer.from(image).toString('base64');
  // const b64_pdf = Buffer.from(pdf).toString('base64');
  // har_extended['log']['pages'][0]['renderedElements'] = [{
  //               selector: ":root",
  //               format: "PNG",
  //               content: b64_image,
  //               encoding: "base64"
  //             },{
  //               selector: ":root",
  //               format: "PDF",
  //               content: b64_pdf,
  //               encoding: "base64"
  //             }];

  // Write out the extended HAR:
  let timestamp;
  for (const header of har_extended.log.entries[0].response.headers) {
    if (header["name"] === "Memento-Datetime") {
      timestamp = header["value"]
      break
    }
  }
  timestamp = new Date(timestamp).toISOString()
  let hash = crypto.createHash('md5').update(seed).update(timestamp).digest('hex')
  await promisify(fs.writeFile)('/output/' + hash + '.har', JSON.stringify(har_extended));

  // Shut down:
  await browser.close();
})();


async function autoScroll(page){
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight || totalHeight > 4000 ){
                    clearInterval(timer);
                    // Scroll back to the top:
                    window.scrollTo(0, 0);
                    resolve();
                }
            }, 200);
        });
    });
}

async function clickButton( page, buttonText ) {
  await page.evaluate(query => {
      const elements = [...document.querySelectorAll('button')];

      // Either use .find or .filter, comment one of these
      // find element with find
      const targetElement = elements.find(e => e.innerText.toLowerCase().includes(query));

      // OR, find element with filter
      // const targetElement = elements.filter(e => e.innerText.includes(query))[0];

      // make sure the element exists, and only then click it
      targetElement && targetElement.click();
  }, buttonText.toLowerCase());
}

async function clickKnownModals(page) {
  // Click known common modals:
  await clickButton(page, "I Accept");
  await clickButton(page, "I Understand");
  await clickButton(page, "Accept Recommended Settings");
  await clickButton(page, "Close");
  await clickButton(page, "OK");
  await clickButton(page, "I Agree");

  // Press escape for transient popups:
  await page.keyboard.press('Escape');

  // Click close on a class of popup observer at https://www.britishdeafnews.co.uk/
  // Doesn't seem to work!
  await page.evaluate(async () => {
      const elements = [...document.querySelectorAll('a.ppsPopupClose')];
      const targetElement = elements[0];
      // make sure the element exists, and only then click it
      targetElement && targetElement.click();
  });

}
