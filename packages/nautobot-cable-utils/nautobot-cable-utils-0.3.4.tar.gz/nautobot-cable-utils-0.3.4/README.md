# Nautobot Cable Utilities

Utilities for working with cables in Nautobot. Enables you to change cable
endpoints and work with cable templates.

Please note that this plugin uses internal Nautobot components, which is
explicitly discouraged by the documentation. We promise to keep the plugin up
to date, but the latest version might break on unsupported Nautobot version.
Your mileage may vary.

## Installation

The plugin can be found on [pypi](https://pypi.org/project/nautobot-cable-utils).
You should therefore be able to install it using `pip`:

```
pip install nautobot-cable-utils
```

Make sure to use the same version of `pip` that manages Nautobot, so if you’ve
set up a virtual environment, you will have to use `<venv>/bin/pip` instead.

After that, you should be able to install the plugin as described in [the
Nautobot documentation](https://nautobot.readthedocs.io/en/stable/plugins/). No
change to `PLUGINS_CONFIG` is necessary.

## Usage

This plugin has two main purposes: [reconnecting cables](#reconnecting-cables)
and [working with cable templates](#working-with-cable-templates).

### Reconnecting cables

If you want to reconnect a cable, just go to its detail view. There should be a
button called `Reconnect` that will send you to a form in which you can change
cable endpoints.

<img alt="Reconnect button" src="./docs/reconnect_button.png" width="150">

The form that it will send you to is fairly similar to the cable creation view,
but it will not allow you to edit the cable’s properties.

![Reconnect form](./docs/reconnect_form.png)

### Working with cable templates

Cable templates can be found under `Plugins`, where you will be able to add them
one by one or import them via CSV (both buttons next to `Cable templates`). They
have all the same properties as regular cables, plus a cable number.

<img alt="Cable template form" src="./docs/template_form.png" width="500">

Cable templates can be used in any planned cable. If you navigate to that
cable’s detail view, an additional button named `Commission` will appear.

<img alt="Commission button" src="./docs/commission_button.png" width="150">

If you click on it, you will be able to select the cable template you want to
use for it (by cable number). The cable takes on the properties of the template
(length, color, etc.) and the template will not be selectable again for future
cables.

If a cable template should be removed or changed the function `Undo Commission` can be used. On a previously commissioned cable which uses a valid template this button will appear

<img alt="Undo Commission button" src="./docs/undo_commission_button.png" width="180">

By pressing this button  the commissioned cable will be removed but the cable trace will be left unaffected. A planned cable will take place which can be commissioned with another cable template if wanted.

#### Bulk Commission on Devices

To save time a bulk commission function can be used directly out of a selected device. If a device has planned cables an additional button `Device Commission` will appear:

<img alt="Device Commission button" src="./docs/device_commission_button.png" width="180">

By pressing this button all cables will can be commissioned in a loop.

<img alt="Device Commission form" src="./docs/device_commission_form.png" width="800">

The form shows you some important information while commissioning cables. On the top the amount of planned cables on the current device is shown. On the left hand side the connection details and on the right hand side the input field for a cable template are displayed.

By pressing the button `Create` the current cable will be commissioned with the selected (cable)template. By using the button `Skip` the current cable will be left out and the next planned cable is displayed. By pressing `Cancel` the bulk commission will stop and you will be redirected to the previously selected device. After one cable is created or skipped the next planned cable will be displayed.  

<b> Important Note! </b>This process is session-dependent. If the form is unexpectly closed or left without pressing the `Cancel` button the current process of the form is paused and will be continued at the same point if re-opened until the current session has expired or another device is selected. To review skipped cables the form must be exited by pressing `Cancel` and freshly opened.

<hr/>

Have fun!
