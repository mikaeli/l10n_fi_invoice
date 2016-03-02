Finnish Invoice RF
==================

#### Version: 0.3.1

This is RF-version of Finnish invoices by Avoin Systems.
RF-modification was made by Mikael Ikivesi as our Co-Operative
customers use European banking requiring the use of RF-bank references.
Used RF-reference has Finnish checksum included and work also with Finnish banks.


### Usage

Just install and use.
This add-on creates Finnish template for emailing the invoice,
but will not replace the default odoo email template.



### Possible issues


#### Report.url must be set

If the invoice get printed wrong you probably need to set
report.url system parameter. This is not set in default installation.
To set it you first need to enable Technical features
from user settings. Refresh the browser cache to apply changes
and access Techinical->Parameters->System parameters.
Add/edit report.url with correct hostname and port.
(Most probably http://localhost:8069)


#### Note about fonts

Invoice output quality depend on fonts that python-reportlab can find.
In server environments font availability is usually quite limited.
If your invoices appear pixelated consider installing proper fonts under
reportlab directories. For unix systems this directory is usually:
/usr/local/lib/python2.7/site-packages/reportlab/fonts

