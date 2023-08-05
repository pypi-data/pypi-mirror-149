# ML Engineer Assignment

Thank you for applying to Hubs. We want to assess your abilities as a ML Engineer candidate. You have two options:

1. The assignment described below.
1. A personal project that you think reflects a similar range of skills. You can share with us the code and results, which we will assess and discuss before a technical interview with you.

Both options require the code to be written in Python. If you choose to do this assignment, you’ll find a dataset regarding the price of manufacturing different 3D models. You’ll have 1 week to submit your work. We expect you to spend around 4 hours on this assignment, but it’s your decision to spend as much as you see fit.

After you submit your assignment, our team will review it and if it passes our filters, we'll invite you to a technical interview where we can dig deeper on what you've done and continue from there. 

## Assignment

Hubs is a distributed manufacturing platform. When a customer uploads a part, we find the most appropriate supplier for manufacturing and make sure they receive their order in a timely manner and up to the quality requirements. One of our team’s goals is to understand and predict the price of manufacturing parts based on the customer choices (material, technology, finish, etc.) and geometry. Here, we present you a dataset that contains manufacturing prices for different parts. The assignment can be split in the following steps:
1. Build a simple pipeline that can prepare the data for training and update your model.
1. Build a baseline Machine Learning model to predict the price of the parts. You can use any framework you are comfortable with, we use pytorch :).
1. Analyze the performance of the model, e.g. what are some relevant performance metrics?
1. Encapsulate your model in a way that would make it easier to use by other developers (not necessarly Data Scientists). You can use whatever approach you are comfortable with or find suitable (e.g. dockerfile, package, script+requiremenmts, flask...). Define and implement the inference input and the output of your model as part of this step (given the time constraints, it is not necessary to validate the inputs).


Please be aware that a better ML model isn’t necessarily better, you shouldn’t spend all your time in the ML. We will look at the assignment as a whole, we’ll also pay close attention to the analytical skills and code clarity.

### Instructions

You should create a new branch of this repository and commit and push all the code you wrote together with the results. 
When you're done, create a Pull Request from your branch and we will be notified and will review it.

Please indicate in a `instructions.md` file how we should run your code and what are the components of your solution.

Please avoid commiting very big and unnecesary files to this repository. 

### Dataset

In `assignment-data.csv.zip` you can find a zipped CSV file with the dataset for the assignment. Each row of the dataset represents a 3D geometry that was manufactured at the price given in the column `target/price`. Please note that the parts that share a cart were all manufactured together in the same batch.
This is the list of features:

| Variable | Meaning |
| -------- | --------|
| `timestamp` | Date and time when the part was manufactured. |
| `cart` | Id of the cart. All items in the same cart were manufactured in the same batch. |
| `geometry/bounding_box/depth` |	Depth of the bounding box, in mm. |
| `geometry/bounding_box/width` | Width of the bounding box, in mm. |
| `geometry/bounding_box/height` | Height of the bounding box, in mm. |
| `geometry/bounding_box/volume` | Volume of the bounding box, in mm. |
| `geometry/area` | Surface area of the 3D model, in mm2. |
| `geometry/volume` | Volume of the 3D model, in mm3. |
| `geometry/machining_directions/count` | Number of necessary machining directions to manufacture this part. |
| `options/quantity` | Number of units to be manufactured. |
| `options/lead_time` | Number of days the supplier has to manufacture the order. |
| `options/material_group` | Type of material to be used (real example: "Stainless Steel"). |
| `options/material_subgroup` | Subgroup of the material to be used (real example: "Stainless Steel 304L"). |
| `options/surface_finish` | Finish to apply to the surface of the part (real examples: "Bead blasted", "Anodyzed Type III (Hardcoat)"). |
| `sourcing/supplier_country` | Country of the supplier. |
| `sourcing/supplier` | Supplier identifier. |
| `target/price` | Price of manufacturing all the ordered units of this 3D model. |
