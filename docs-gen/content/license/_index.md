---
title: License
weight: 30
chapter: false
---



## Which license applies

VSS as well as the VSS-tools are covered by the [Mozilla Public License 2.0 (MPL-2.0)](https://opensource.org/licenses/MPL-2.0). The MPL-2.0 is an OSI approved Open Source license that gives you a lot of freedom using VSS in your products, or for (academic) research while providing a solid legal framework should you choose to contribute to either the standards or the tools.

We will line out some answers to commonly asked question, but keep in mind this page is informational. The legally binding clauses can be found in the [license](https://opensource.org/licenses/MPL-2.0) itself. If in doubt, consult your friendly neighborhood lawyer or IP department.

## Can I use VSS / VSS-tools in my commercial products
Most definitely yes. You must inform your users that the product contains MPLed code and need to provide access to the source (e.g. by linking to this documentation or our[our Github repository](https://github.com/covesa/vehicle_signal_specification)).

## I modified VSS-tools, do I need to give away my source?
If you use the code internally within your organisation (company), you have no obligations to do so. (see also [Q5 here](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)). If you distribute the modified vss-tools outside your organization (e.g. to your customers), you need to make the source code of the MPL-2.0 licensed parts available.  However, the MPL has only a very weak copyleft effect. As a rule of thumb: You have no obligation to provide code in new files. You have the obligation to make code of changed existing MPLed files available under the clauses pof the MPL-2.0, _if_ you distribute them in source or compiled form outside your organisation ((see also [Q9,10,11 here](https://www.mozilla.org/en-US/MPL/2.0/FAQ/))).

In any case we _do_ recommend you to consider sharing generally useful improvements with the community. Not only will you win karma points with the community and gain visibility as an innovation leader in the automotive industry, you will most likely also get more robust software as you will have more users and testers. 

## I changed VSS or added custom signals to the standard catalogue. Do I need to give them away?
No. One important selling point of VSS is, that you can always extend the standard catalogue with your own use case specific signals. There is no obligation to release any added signals or proprietary information to third parties.

From an MPL-2.0 point of view the information of the previous question applies. To be extra sure, put any additions in separate files, and use the layering approach to modify the standard catalogue. This community does not consider deleting elements from the standard catalogue or adding VSS `#include` statements "modifications" in the sense of clause 1.10 of the MPL-2.0. 

As with the tools, we _do_ recommend you to consider sharing generally useful standard catalogue improvements with the community. 


