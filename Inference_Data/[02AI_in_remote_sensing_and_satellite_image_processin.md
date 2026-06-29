---
creation_date: "D:20260218030315+01'00'"
modification_date: "D:20260218030315+01'00'"
source_file: [02AI_in_remote_sensing_and_satellite_image_processin.pdf
---



---

**Page 1**


Environmental Earth Sciences (2026) 85:78
https://doi.org/10.1007/s12665-025-12798-w
REVIEW ARTICLE
AI in remote sensing and satellite image processing-a review
Ondrej Krejcar1 · Hamidreza Namazi2,3
Received: 24 July 2025 / Accepted: 24 December 2025 / Published online: 29 January 2026
© The Author(s) 2026
Abstract
The integration of artificial intelligence (AI) in remote sensing and satellite image processing has significantly transformed
the field, offering advanced tools for data analysis, feature extraction, and environmental monitoring. With the growing
availability of high-resolution satellite imagery, AI applications such as machine learning and deep learning have been
applied to automate the process of interpreting complex spatial data. This paper intends to explore the current state of
AI in remote sensing, focused on some applications such as land cover classification, object detection, climate change
monitoring, and disaster management. Additionally, the challenges and future directions for AI-driven remote sensing are
discussed, emphasizing the need for better generalizability, data fusion, and improved computational efficiency.
Keywords Artificial intelligence · Remote sensing · Satellite image processing · Machine learning · Deep learning ·
Environmental monitoring · Data fusion
Introduction There is an AI approach to tackling the unique and very
complex nature of remote sensing data. AI finds the solu-
Remote sensing, using satellite or airborne sensors for the tions in machine learning (ML) and deep learning (DL)
detailed investigation of the earth's surface, has become techniques, as they provide the power to automate the
indispensable in tackling global and local problems, such analyses of large geospatial datasets, the discovery of pat-
as environmental conservation, precision agriculture, urban terns, and the extraction of valuable information. By using
planning, and natural disaster response. Modern advance- sophisticated algorithms, AI enables understanding of
ments in the technology of sensors have generated a massive subtle spatial, temporal, and spectral variations in satellite
amount of functional data, which has enlarged the variety imagery that normally would go undetected by conventional
and resolution of satellite imagery retrieval, thus enabling methods (Rao et al. 2024). For example, through models
more accurate and extensive visibility monitoring of ter- built upon AI principles, urban expansion patterns can be
restrial, atmospheric, and marine environments (Chibuike detected, changes can be seen in land cover, crop health
and Nzeanorue 2024). However, with the booming out of can be monitored, and devastation impacts can be assessed
data came additional burdens on managing, analyzing, and (Zhujun and Maimai 2023).
interpreting the newly drawn-out huge amounts in time and Machine learning techniques such as support vector
space (Zhipeng et al. 2023). machines (SVMs), random forests, and k-means clustering
have been used in remote sensing for some time for land
cover classification and vegetation monitoring (Firas et al.
2024; Asif et al. 2024). However, this new evolution has
Hamidreza Namazi widened the capability of AI applications in remote sens-
Hamidreza.namazi@monash.edu
ing, as deep neural networks (DNNs), convolutional neural
1 Center for Basic and Applied Research, Faculty of networks (CNNs), and recurrent neural networks (RNNs)
Informatics and Management, University of Hradec Kralove, allow the models to learn complex data hierarchies as well
500 03 Hradec Kralove, Czech Republic as directly drive from raw imagery. Thus, deep learning
2 Skoda Auto University, Na Karmeli 1457, Mlada Boleslav, models are used for better effectiveness in the analysis of
Czech Republic high-resolution imagery and multidimensional data (e.g.,
3 School of Engineering, Monash University, Selangor, multispectral or hyperspectral images) and for accuracy
Malaysia
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 2**


78 Page 2 of 10 Environmental Earth Sciences (2026) 85:78
improvement in object detection, segmentation, and feature high accuracy in road extraction from high-resolution
extraction (Tachasit et al. 2024). orthophoto images, with average precision, recall, F1 score,
This review paper highlights the wide-ranging applica- overall accuracy, and IOU percentages of 91.09%, 95.32%,
tions of AI in remote sensing and satellite image processing, 93.15%, 94.44%, and 87.21%, respectively (Abdollahi et al.
including the most recent developments and ongoing chal- 2021). In another work, the CNN model effectively classified
lenges, as well as the future potential of AI-centered remote aerial photographs into seven land cover classes, including
sensing. We shall discuss different use cases, including roads, achieving an overall accuracy of 0.973 and a Kappa
environmental monitoring, where AI shapes outcomes on coefficient of 0.967, demonstrating its capability for accu-
changes in deforestation, biodiversity losses, and impacts rate differentiation of various land cover types, including
of climate change; agricultural processes that take advan- roads (Sameen et al. 2018). Hybrid architectures combin-
tage of an AI's potential to minimize crop stress, optimal ing deep CNNs with random forests have also been applied
irrigation, and yield prediction; and many other examples to in agricultural land classification, showing that integrating
come. The challenges with AI in remote sensing and satel- traditional ML with DL can enhance accuracy in heteroge-
lite image processing will also be discussed and will be used neous regions. For instance, an interesting work proposed
to develop guidelines for future works. a CNN-Random Forest Hybrid model for phenology-based
paddy rice mapping, achieving an overall accuracy of 0.950.
This approach effectively integrates deep learning with tra-
Applications of AI in remote sensing ditional classification methods, enhancing agricultural land
classification using multi-temporal satellite imagery (Sudi-
Land cover and land use classification ana et al. 2025). Together, these applications demonstrate
that CNNs not only advance computational efficiency but
Land cover and land use classification are critical compo- also directly support biodiversity monitoring, urban expan-
nents of remote sensing, as they provide essential infor- sion tracking, land degradation assessment, and sustainable
mation for understanding environmental changes, urban land management.
development, agricultural activities, and ecological health Another approach that has gained traction is the use of
(Firas et al. 2024). The application of AI has resulted in transfer learning, which allows pre-trained deep learning
impressive advantages, enhancing the users' ability to effec- models to be adapted for specific land cover classification
tively and efficiently classify tasks using deep learning and tasks. This approach has proven particularly useful when
machine learning models. labeled data are scarce, as it reduces the need for large,
Traditional methods for classifying land cover face labeled training datasets (Matteo et al. 2024). A case in point
severe obstacles from the complexity induced by the diver- is the study (Liu and Wang 2024) in which land cover clas-
sity of landscapes and the data volume available from sat- sification in rural settings was undertaken with the help of
ellites: maximum likelihood classifiers and support vector a pre-trained ResNet and land cover classification through
machines (SVMs) (Gadiparthi et al. 2024). Recently, deep transfer learning, demonstrating a considerable enhance-
learning, particularly through convolutional neural networks ment even when using limited unlabeled data. This means
(CNNs), has emerged as a key method for addressing the that transfer learning might be a better alternative for devel-
problems arising from the preceding classifiers. With their oping countries or regions with very resource-intensive
high capacity for automatically learning spatial patterns labeled data collection.
from high-resolution images and extracting key features, Attention mechanisms have been integrated into deep
CNNs are particularly effective when it comes to differen- learning models to improve the precision in land cover clas-
tiating accurately between the various types of land covers. sification. Attention mechanisms allow an emphasis on the
Recent research further demonstrates that CNN-based most informative image regions, thereby facilitating better
models are now being applied beyond generic object rec- feature extraction (Zhipeng 2024). An instance is the work
ognition, with direct implications for environmental earth presented in Abhiroop et al. (2024), where the attention-
sciences. For example, CNN architectures have been suc- based CNN model for land use classification was imple-
cessfully used to map deforestation patterns in tropical mented, demonstrating that the attention module could
forests (Pozzobon de Bem et al. 2020), monitor vegetation greatly enhance the model in identifying subtle differences
stress through integration with spectral indices such as NDVI between similar land cover classes.
(Tufail et al. 2025). At the same time, several technical stud- Random forests and gradient boosting machine models
ies have highlighted their superior performance in urban are currently in widespread use, particularly in projects with
and peri-urban environments. For instance, an interesting interpretability and simplicity demands (Giulia et al. 2023).
study demonstrated that the CNN-based method achieved These methodologies achieved successful classification of
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 3**


Environmental Earth Sciences (2026) 85:78 Page 3 of 10 78
agricultural and forested sites when combined with spec- Traditional methods, such as edge detection and template
tral indices like Normalized Difference Vegetation Index matching, have limitations regarding handling the features
(NDVI) and Enhanced Vegetation Index (EVI) (Nayak and of diversity, scale, orientation, and complexity in satellite
Panda 2024). imagery (Hewa et al. 2024). These limitations can be over-
Recent years have seen an increase in the exploration of come by AI-based techniques, particularly through CNNs
self-supervised and semi-supervised learning techniques to that automatically learn and derive spatial hierarchies.
address the challenge of limited data. This form of learn- For instance, a study (Hou and Jing 2024) used R-CNN in
ing gives the model knowledge of feature representations detecting buildings and vehicles within the semiconfined
by using vast amounts of unlabeled satellite imagery, which spaces of very urbanized areas and reported remarkable
is further fine-tuned for specific classification tasks (Jayanth improvements in precision against traditional methods.
et al. 2024). For instance, a study (Wenqing et al. 2024) used Other authors (Yash et al. 2024) used the YOLO (You Only
a self-supervised learning approach to land cover classifica- Look Once) model to detect agricultural features like crop
tion and showed improvements in the performance of deep fields and irrigation systems. They concluded that YOLO's
learning models with land cover classification tasks on lim- high speed and accuracy greatly favor it for large-scale agri-
ited labeled data, thereby reducing the dependency on labor- cultural monitoring. In addition, a recent study (Rajasekhar
intensive labeling efforts. 2024) used YOLO to detect and identify various land cover
Overall, AI-driven land cover and land use classification types in satellite images, showing its potential for quick
have made some meaningful advances in accuracy, effi- analyses in applications needing to cover large areas.
ciency, and automation. The collision of deep learning with Feature extraction is a prerequisite and a significant
transfer learning, attention mechanisms, and self-supervised component in converting raw satellite images into valu-
learning has transformed the remote sensing data process- able information through quantifying shape, texture, spec-
ing, giving rise to more detailed and accurate assessments tral characteristics, and spatial relationships (Xizhen et al.
of environmental and urban dynamics. 2024). For example, studies (Potić et al. 2023) have com-
bined spectral indices such as the Normalized Difference
Object detection and feature extraction Vegetation Index (NDVI) with machine learning models,
including support vector machines (SVMs), to classify
Object detection and feature extraction form two major types of vegetation at high accuracy levels in forested and
applications of artificial intelligence in remote sensing-the agricultural areas.
accurate identification and classification of objects from sat- Recent innovations in AI bring attention mechanisms
ellite imagery. AI models have been significantly developed and multi-task learning frameworks that aim at improving
to detect various features like buildings, roads, vegetation, object detection performance in remote sensing applications
water bodies, and land-use patterns, which have all brought (Danqing and Yiquan 2023; Sadique et al. 2024). For exam-
about benefits to urban planning, environmental monitoring, ple, researchers (Ashen and Hewarathna 2024) developed
resource management, and more. Researchers (Valliappan an attention-based CNN model for monitoring deforesta-
et al. 2024), for example, had developed and applied convo- tion patterns, such that the attention mechanism focuses on
lutional neural networks (CNNs) to identify urban structures regions that are integral to improving the accuracy of clas-
in high-resolution satellite images, whereby they achieved sification for expansive, heterogeneous forest landscapes.
over 90% in classification tasks and further supported urban Transfer learning has also gained popularity, as it enables
planning by detailed urban layouts. Likewise, coastal infra- models pre-trained on large datasets to be adapted to specific
structure monitoring was conducted by studies through the remote sensing tasks with minimal additional training (Yuan
CNN-based object detection approach, which proved to be et al. 2023; Albughdadi et al. 2024). Researchers (Feng and
very sensitive in detecting changes. For instance, a study Yuan 2024) have employed transfer learning using fine-tun-
utilized a CNN to detect breaking points, crest orientation, ing in region-specific datasets, demonstrating the improve-
and relative Still Water Level (SWL) in surfing waves, ment in accuracy in distinguishing among urban, suburban,
achieving a mean Average-Precision (mAP) of 0.794, dem- and rural landscapes. Another study found that a ResNet50
onstrating its effectiveness in monitoring dynamic coastal model pre-trained on the RESISC-45 dataset achieved the
resources (Atkin et al. 2023). Another work implemented highest accuracy of 97.10% when classifying the Eurosat
CNN-based semantic segmentation for monitoring coastal dataset, demonstrating the effectiveness of transfer learning
surface changes, achieving a global accuracy of 93.9% and in remote sensing applications (Failed 2022).
an Intersection over Union (IoU) range of 86.6–92.7%, To sum up, advancements in artificial intelligence for
effectively detecting changes in classes like mangrove, veg- object detection and feature extraction are changing the sce-
etation, sand, and sea (Padilla-Arballo et al. 2022). nario of remote sensing by analyzing satellite images more
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 4**


78 Page 4 of 10 Environmental Earth Sciences (2026) 85:78
accurate and effective. The monitored detail can be done on early warning systems for biodiversity protection (Narciso
the environmental and human-made constructions, as the et al. 2024). In yet another study, researchers applied the
value of these techniques increases from sustainable devel- long short-term memory (LSTM) model to analyze ocean
opment to disaster management applications. temperature data for predicting marine heatwave events (Qi
et al. 2024).
Climate change monitoring In addition, climate-driven events such as wildfires,
droughts, and floods are monitored and forecasted through
Climate change monitoring is a significant application of AI AI-based predictive models, which are fundamental in
in remote sensing that provides a better understanding of disaster preparedness. For example, machine learning was
environmental changes, greenhouse gas emissions, land-use used to predict the risk of wildfires with the incorporation
changes, and natural resource dynamics (Chuanming 2024). of weather and land-use datasets, such as air temperature,
These tools offer vast amounts of data collected using vapor pressure deficit, NDVI, and fuel moisture, attain-
sensors, and this data can be used for the assessment and ing 72% accuracy with the most significant predictors for
mitigation of the impacts of climate change. For example, improved predictions (Heechan et al. 2024). Data of this
deep learning techniques have been used to observe the type can be useful for managing water resources, as noted
snow cover changes in mountain regions by adding it as an in another possible drought prediction model (Haitham and
important parameter to trace water resources demarcated by Afan 2024). In addition, floods were predicted through deep
global warming (Pinder 2024). learning trained on rainfall and river flow data for enhanced
For monitoring climate, the conventional methods utilize disaster management in flood-prone regions (Jamunadevi et
manual data analysis and statistical models, which usually al. 2024). An interesting study utilized deep learning mod-
confine the spatial–temporal complexities of data. With AI els, specifically GRU and LSTM, integrating upstream river
models, especially deep learning, large volumes of com- flow, river water level, and tidal level data to enhance flood
plex data can be assessed, analyzed, and processed more prediction accuracy, supporting effective disaster manage-
accurately. For example, one work estimated the seasonal ment in flood-prone regions like the Pattani River basin
CO₂ emission in both urban and rural settings by applying (Duangkhwan 2025). Another work discussed an AI-based
satellite data through recurrent neural network-based analy- framework for multi-risk assessment in the Veneto region,
sis, thus providing information on anthropogenic impacts integrating single hazard susceptibility maps and socio-eco-
on greenhouse gas levels (Zhonghua et al. 2024). Another nomic vulnerability indicators to enhance understanding of
work espoused real-time monitoring on methane emissions extreme climate events, particularly focusing on heatwaves,
through an AI model that integrated satellite observations droughts, and their impacts on tourism and agriculture (Fer-
with analytic predictions to track methane sources and rario et al. 2025).
trends in the agricultural and industrial sectors (Anna, et al. In short, AI has transformed climate change monitoring
2024). through large-scale, automated analysis of environmental
The health of forests and land-use changes significantly changes. With machine learning, deep learning, and pre-
impact climate monitoring, as they are the primary sources dictive modeling combined, researchers can now monitor
of greenhouse gas emissions and biodiversity loss (Nicole et climate indicators across different sectors and topics. These
al. 2024). One study established deep learning-based object developments translate into better-informed decisions sup-
detection algorithms to monitor illegal logging and forest portive of climate resilience, conservation, and environmen-
degradation in the Amazon rainforest with over 90% accu- tal policy, contributing toward global sustainability.
racy (Gupta et al. 2024). Another research investigated ran-
dom forest and spectral indices like NDVI for monitoring Disaster management
tropical deforestation to generate the necessary actionable
data for conservation and reforestation (Ana et al. 2023). AI has significantly enhanced disaster management by
AI models are also instrumental in tracking oceanic and systematically analyzing vast volumes of real-time remote
atmospheric conditions to better understand sea level rise, sensing datasets, enabling speedy mitigation responses to
ocean temperature variations, and extreme weather pat- chronic events such as earthquakes, floods, wildfires, hurri-
terns. Deep neural networks were applied by researchers to canes, and landslides. AI models help to emphasize the level
analyze satellite data for sea level rise and coastal erosion, of destruction, predict appropriate locations for more disas-
thus generating maps of flood-prone areas with good accu- ters, and ensure the proper distribution of resources during
racy (Khadar et al. 2024). Another use of machine learn- crises. For instance, this study (Guangxing and Gwanghyun
ing was to monitor coral bleaching and marine ecosystem 2024) utilized convolutional neural networks (CNNs) for
health in response to rising ocean temperature, thus aiding the analysis of objects (like buildings and infrastructural
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 5**


Environmental Earth Sciences (2026) 85:78 Page 5 of 10 78
objects) in hurricane-hit areas, identifying destroyed build- Storm and hurricane monitoring and impact assessments
ings and infrastructure, which enabled efficient relief efforts are also surveyed by AI. Researchers have constructed
in the most affected areas. Likewise, in another study (Fur- a hybrid deep learning model to analyze meteorological
kan et al. 2024), deep learning was employed with post- data from satellite to predict flooding with high accuracy
disaster satellite imagery to assess the damage following an (Abdelkader et al. 2024). Researchers also performed trans-
earthquake, thereby increasing the classification of damage fer learning on AI trained by historical hurricane data to pre-
via automatic means. dict storm surges (Stefanos et al. 2024).
Classical disaster management stands to be rudimen- Generally, AI in the field of disaster management,
tary, being persistently dependent on manual assessment depending on the power it garners from remote sensing,
and scant analytical capacities (Shailen 2023; Grimaz et al. augments emergency preparedness, real-time response, and
2023). Thus, called deep learning, the AI approach proves to post-disaster relief. AI models expedite response times, bet-
be more prompt as well as accurate. Similarly, some of the ter fitting resource provision, and damage assessment accu-
latest research used machine learning to predict flood risks racy in coping with diverse nature(scale)-related disasters.
given topographic and meteorological data, which would
assist in the precision prediction of regions to prioritize in
responding to a flood. For instance, a study (Shrestha et al. Challenges in AI-Driven remote sensing
2025) utilized machine learning algorithms, including logis-
tic regression, to analyze topographical and meteorological Marked by prominent gains in the field of remote sensing,
data for flood risk assessment in Charlotte, North Carolina, artificial intelligence (AI) allows significant automation fea-
effectively identifying and prioritizing regions for emer- tures, pattern detection, and data insight into transmission.
gency preparedness and infrastructure planning based on However, the integration of AI into the processing of satel-
flood susceptibility. Another work utilized machine learning lite images faces challenges. All such challenges impact the
models, incorporating 13 explanatory variables from topo- growth and use of AI in remote sensing applications. Thus,
graphical, hydrological, and environmental data, to create some of these challenges need to be overcome to utilize AI
flood susceptibility maps for Thessaly, Greece, enhancing for optimal benefit in environmental monitoring, disaster
precision in predicting flood-prone regions and aiding in management, urban planning, etc. Here, we discuss some
disaster preparedness and response planning (Tepetidis et of the main challenges implicated in applying AI to remote
al. 2025). sensing and satellite-image processing.
The recent progress in AI technologies for wildfire Quality and Availability of Data: The availability of
monitoring is enormous. A curious study used deep learn- high-quality, labeled data remains a core challenge in AI-
ing techniques for the fusion of satellite and drone images driven remote sensing (Mingyuan et al. 2024). Many AI-
to ascertain wildfire hotspots, predict spread potential, and based models, in particular deep learning models, require
provide input on environmental damage (Devi et al. 2024). large, diverse, well-annotated datasets for the training pro-
Another study highlights the integration of drone-captured cedure to warrant high accuracy and good generalization
images with deep learning algorithms for autonomous wild- (Surbhi et al. 2024). In terms of remote sensing, however,
fire detection, achieving over 97% accuracy and over 99% labeled datasets tend to be quite limited, especially in spe-
precision using an ensemble approach, significantly enhanc- cialized applications or in areas where labeled imagery is
ing early pile fire detection capabilities compared to tradi- simply limited or not available (Maximilian et al. 2024).
tional methods (Joshi et al. 2024). Moreover, acquiring high-resolution satellite imagery can
Another vital application is the detection of earthquake be costly, with the spatial, spectral, and temporal resolutions
damage via AI models in disaster management. A study from different sensors potentially being so different as to
(Ilmak et al. 2024) developed an efficient deep learning- pose challenges to data harmonization (Else et al. 2022).
based system, analyzing Maxar's high-spatial-resolution Open access data sharing and synthetic data generation are
satellite imagery to separate the post-earthquake buildings other ideas, but again, data quality and adherence remain the
into classes of collapsed and non-collapsed, thus arming the major challenges.
emergency respondents with an even more efficient way of Computational Complexity: The requirements for deep
assessing damage. Another study (Divya et al. 2024) used learning processing in remote sensing are considerable,
AI coupled with synthetic aperture radar (SAR) data in the especially when high-resolution or multispectral imagery
detection of landslide-prone areas, furnishing very use- containing data points of high volume is concerned. In fact,
ful insights toward regions that highly deserve immediate the training and deployment of these very models require
evacuation efforts and appropriate infrastructure planning. hardware resources of high power, often GPUs or TPUs,
which may not be accessible to the majority of organizations,
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 6**


78 Page 6 of 10 Environmental Earth Sciences (2026) 85:78
especially in such resource-constrained settings. Feasibly, Future directions
these are highly computationally intensive AI models, limit-
ing their application to real-time processing, which remains There is a bright path ahead for AI in remote sensing, with
paramount in disaster responses and the like (Furkan et al. several avenues for innovative research and technology
2024). Model compression and pruning approaches will integration into this field. One future research area would lie
help alleviate some of that pressure, while the integration in multimodal data fusion, where data from different sensors
of cloud or edge computing must also be considered; never- such as optical, SAR, synthetic aperture radar, and LiDAR
theless, semi-efficient real-time processing at a much larger are integrated for a more holistic view of the Earth's sur-
scale remains a significant question. face. The fusion of multispectral, hyperspectral, and radar
Interpretability and Transparency: Many AI models, data can substantially increase the accuracy and robustness
especially deep learning architectures, operate as “black of the AI models, particularly in environments where a sin-
boxes,” making it difficult to understand the decision- gle sensor is inadequate. Thus, AI models performing data
making process behind their predictions (Oku et al. 2024). fusion across several sensors will provide better precision in
This lack of interpretability presents challenges for remote monitoring land-use changes, vegetation health, and natural
sensing applications where transparency is crucial, such as disasters.
disaster management and environmental regulation, where Another development along the way is Explainable
stakeholders need to understand the basis of AI-driven deci- AI (XAI), and this entails much more. Development of
sions. Explainable AI (XAI) research is developing solu- explainable AI models will present stakeholders with a
tions to these problems through mechanisms that increase lucid rationale for when and why such models output what
the interpretability of AI models. Nevertheless, relatively they do, for purposes of awesome transparency and winning
few solutions are already in the market for actual end-user trust. This is particularly important for critical applications,
applications in remote sensing. including disaster response, environmental monitoring, and
Data Fusion and Integration: Remote sensing is often urban planning, where AI-driven decisions can have signifi-
data integration from different sources, such as multispec- cant societal and economic implications. The XAI methods
tral, hyperspectral, radar, and thermal sensors, and ancillary thus developed, such as saliency maps, attention mecha-
data such as weather data or field measurements (Mengmeng nisms, and feature attribution, should all serve to improve
et al. 2023). It is the challenge of integrating these diverse the interpretability of the AI models without sacrificing
types of data into coherent, accurate models that adds to the performance.
complexity, owing to disparities in data format, resolution, The amalgamation of AI and edge computing looks to
and acquisition conditions. To derive trustworthy informa- position itself beautifully in the future of remote sensing.
tion, AI models would need to learn efficiently from these Edge computing enables real-time processing of satellite
heterogeneous datasets; however, data fusion is difficult and data directly on the sensors or nearby, resulting in faster
resource-intensive. Some progress is being made in real-life decision-making due to reduced latency (Jinming et al.
applications of multimodal learning and sensor fusion tech- 2024). This is particularly useful for any time-sensitive
niques, but this process is still evolving, especially in the application, such as a natural disaster response and emer-
context of large-scale implementations. gency management, where processing the right informa-
Generalization and Transferability: Generalization is tion in a timely manner can save lives and reduce damage.
hard for many AI models trained on certain datasets when Advances in lightweight AI models and edge computing
applying them to new instances or regions, sensors, or envi- hardware will further favor the prompt processing of satel-
ronmental conditions (Friedman et al. 2024). For example, lite data on-site and render remote sensing technology better
a model trained for vegetation pattern assessment in a equipped to respond and adapt to changing conditions.
given area may not do so well in a different ecosystem or Another aspect that may revolutionize AI-based remote
climatic setting (Rebecca and James 2024). This predica- sensing is federated learning. Federated learning allows
ment thwarts generalization and creates a big hurdle for models to be trained in cooperation from different data cen-
AI in remote sensing, whereby the applicability of models ters while keeping raw data siloed, thus preserving data pri-
across various geographic locations or climatic contexts vacy and security (Balamurugan 2024). Federated learning
is limited. Transfer learning, self-supervised learning, and in remote sensing will facilitate cross-border collaborations,
domain adaptation techniques appear as a light at the end allowing institutions from different regions to train models
of the tunnel, allowing the adaptation of the model to the based on datasets without revealing sensitive information.
new environment with minimal additional data. Yet, these This will not only improve the generalization of models but
require maturity for consistent performance through varying also culminate in international collaborations on monitoring
remote sensing tasks.
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 7**


Environmental Earth Sciences (2026) 85:78 Page 7 of 10 78
such global phenomena as climate change, deforestation, Though these advancements are highly promising,
and disaster management. numerous challenges remain, especially concerning data
In addition, advances in transfer learning and self-super- quality and computational requirements, interpretability of
vised learning are expected to play a critical role. Transfer models, and generalizability of an AI model across different
learning employs AI models that have been trained in one geographies and environmental settings. This will require
domain with vast datasets and then fine-tuned for task-spe- continuous investment in high-quality datasets, more robust
cific applications in remote sensing to reduce the amount computational infrastructure, and the interpretation as well
of labeled training data. As for self-supervised learning, as scalability of models that can take on the ambiguities and
where models are capable of learning from unlabeled data, complexities of remote sensing data.
the technique has proven invaluable in leveraging large In all likelihood, the future of AI in remote sensing will
amounts of unannotated satellite imagery for downstream be promising, particularly regarding breakthroughs such as
improvements in the classification, segmentation, and multimodal data fusion, explainable AI, edge computing,
anomaly detection models' performance (Ali and Hossein and federated learning. This will render AI-aligned remote
2024). sensing not only more efficient and effective, but rather,
Another future direction refers to the use of GANs for significantly lower the bar to access and actionize it for
synthetically generating data. These networks can be used stakeholders of diverse sectors. The impact that AI models
for the creation of realistic yet synthetic satellite images. will have on sustainable development, disaster resilience,
Such images supplement the existing datasets, hence or environmental stewardship will rise tremendously as
strengthening the models. They address a drawback of lim- the models become increasingly flexible, interpretable, and
ited training data and contribute to improving diversity in cooperative.
the examples used for AI training, with particular attention In summation, AI-driven remote sensing has what it takes
to underrepresented regions. to be a major player in addressing global challenges, deliver-
Recently, increasing interest has been realized in com- ing critical insights, and informing data-driven approaches
bining AI with citizen science and crowd-sourcing data to complex issues. Interdisciplinary collaboration and tech-
(Shu-Wei et al. 2024; Karin et al. 2024; Sameer and Pri- nological innovation will remain crucial in future efforts to
yanka 2024). Merging both satellite imagery and observa- leverage the full potential of AI in remote sensing and its
tions from the ground by citizen scientists would give a beneficial impact on society and the environment.
more complete and well-detailed coverage of much more of
the environment. Thus, AI models that use remote sensing Acknowledgements This work was supported in part by Long-Term
Conceptual Development of Research Organization (2024) at Skoda
data and public information can revolutionize environmen-
Auto University, Czech Republic.
tal monitoring, improve urban planning, and significantly
assist during disaster response. In this way, a more com- Author contribution H.N. & O.K. wrote the manuscript.
prehensive understanding is gained of the dynamics under
which changes occur across the Earth's surface. Funding Open Access funding enabled and organized by CAUL and
its Member Institutions
Data availability No datasets were generated or analysed during the
Conclusion
current study.
The integration of artificial intelligence (AI) in remote Declarations
sensing and satellite image processing has brought new
possibilities across multiple application domains, from Competing interests The authors declare no competing interests.
environmental monitoring to urban planning, from climate
change analysis to disaster management, and so forth. This Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
review highlighted the various AI techniques applied in the
adaptation, distribution and reproduction in any medium or format,
field, such as identifying machine learning, deep learning,
as long as you give appropriate credit to the original author(s) and the
transfer learning, and data fusion approaches that enable source, provide a link to the Creative Commons licence, and indicate
efficient and accurate assessments of the accumulated if changes were made. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless
volume and aggravation of complexities of satellite data.
indicated otherwise in a credit line to the material. If material is not
Hence, researchers, practitioners, and regulators will obtain
included in the article’s Creative Commons licence and your intended
meaningful insights from the data that are otherwise diffi- use is not permitted by statutory regulation or exceeds the permitted
cult to process manually, thus accelerating decision-making use, you will need to obtain permission directly from the copyright
holder. To view a copy of this licence, visit h t t p : / / c r e a t i v e c o m m o n s . o
and proactive responses to global challenges.
r g / l i c e n s e s / b y / 4 . 0 /.
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 8**


78 Page 8 of 10 Environmental Earth Sciences (2026) 85:78
References the Veneto Region. EGU25-16640. h t t p s : / / d oi . o r g / 1 0 . 5 1 9 4 / e g u s p
h e r e - e g u 2 5 - 1 6 6 4 0
Firas A, Mert D, Cevdet Ş (2024) Environmental monitoring of land
Abdelkader R et al (2024) A novel hybrid deep-learning approach for
use/ land cover by integrating remote sensing and machine learn-
flood-susceptibility mapping. Remote Sens. h t t p s : / / d o i . o r g / 1 0 . 3 3
ing algorithms. J Eng Sustain Develop. h t t p s : / / d oi . o r g / 1 0 . 3 1 2 7 2
9 0 / r s 1 6 1 9 3 6 7 3
/ j e a s d . 2 8 . 4 . 4
Abdollahi A, Pradhan B, Pradhan B, Pradhan B, Shukla N (2021) Road
Friedman D, Sadler J, Churchill T (2024) Adaptive neural network
extraction from high-resolution orthophoto images using convo-
architectures for cross-domain generalization. Computer Life
lutional neural network. J Indian Soc Remote Sens 49(3):569–583
12(2):1–5Friedman D, Sadler J, Churchill T (2024) Adaptive
Afan HA et al. (2024) LSTM Model Integrated remote sensing data for
neural network architectures for cross-domain generalization.
drought prediction: A study on climate change impacts on water
Computer Life 12(2):1–5
availability in the Arid Region. Water, h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / w
Furkan K et al (2024) Evaluating fine tuned deep learning models
1 6 1 9 2 7 9 9
for real-time earthquake damage assessment with drone-based
Albughdadi M, Baousis V, Kaprol T, Karatosun A, Pisa C Exploring
images. AI Civil Eng. h t t p s : / / d o i . o r g / 1 0 . 1 0 0 7 / s 4 3 5 0 3 - 0 2 4 - 0 0 0 3
sam transfer learning in optical remote sensing, IGARSS 2024
4 - 6
- 2024 IEEE International Geoscience and Remote Sensing Sym-
Gadiparthi M, Al-Fatlawy RR, Kulkarni M, Malathy V, Anbunathan R
posium, Athens, Greece, 2024, pp. 2519–2523, h t t p s : / / d o i . o r g / 1 0
Land cover classification in high-resolution satellite images using
. 1 1 0 9 / I G A R S S 5 3 4 7 5 . 2 0 2 4 . 1 0 6 4 1 3 2 1
vision transformer and ConvNeXt Approach, 2024 International
Ali G, Hossein S (2024) Self-supervised in-domain representation
Conference on Data Science and Network Security (ICDSNS),
learning for remote sensing image scene classification. Heliyon.
Tiptur, India, 2024, pp. 1–4, h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / I C D S N S 6 2
h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . h e l i y o n . 2 0 2 4 . e 3 7 9 6 2
1 1 2 . 2 0 2 4 . 1 0 6 9 0 9 7 6
Guisao-Betancur A, Gómez Déniz L, Marulanda-Tobón A (2023) For-
Grimaz S, Malisan P, Zorzini F et al (2023) Customisable IT tool for
est/Nonforest Segmentation Using Sentinel-1 and -2 Data Fusion
on-field assessments to support disaster management. Sci Rep
in the Bajo Cauca Subregion in Colombia. Remote sensing, h t t p s
13:21011
: / / d o i . o r g / 1 0 . 3 3 9 0 / r s 1 6 0 1 0 0 0 5
Guangxing W, Gwanghyun Jo (2024) An improved post-hurricane
Asif A, Shaik N, Shaik C, Geetha, Priya. (2024) Predictive modeling in
building damaged detection method based on transfer learning.
remote sensing using machine learning algorithms. Int J Curr Sci
Indonesian J Electrical Eng Computer Sci. h t t p s : / / d o i . o r g / 1 0 . 1 1 5
Res Rev. h t t p s : / / d o i . o r g / 1 0 . 4 7 1 9 1 / i j c s r r / v 7 - i 6 - 6 2.
9 1 / i j e e c s . v 3 3 . i 3 . p p 1 5 4 6 - 1 5 5 6
Atkin EA, Davies-Campbell J, McIntosh R (2023) Deep learning
Gupta R, Ruokolainen K, Tuomisto H (2024) Detection of deforesta-
object detection application to surfing wave quality. Coastal Eng
tion using prisma hyperspectral and deep learning (1DCNN) in
Proc. h t t p s : / / d oi . o r g / 1 0 . 9 7 5 3 / i c c e . v 3 7 . p a p e r s . 2 5
the Amazon Forest," IGARSS 2024 - 2024 IEEE International
Balamurugan M (2024) Federated learning frameworks for secure and
Geoscience and Remote Sensing Symposium, Athens, Greece,
decentralized authentication. Int J Multidisciplinary Res. h t t p s : / / d
2024, pp. 3704–3707, h t t p s : / / d oi . o r g / 1 0 . 1 1 0 9 / I G A R S S 5 3 4 7 5 . 2 0
o i . o r g / 1 0 . 3 6 9 4 8 / i j f m r . 2 0 2 4 . v 0 6 i 0 5 . 2 7 9 0 1
2 4 . 1 0 6 4 2 1 9 6
Chatterjee A, Ghosh S, Ghosh A, Ientilucci EJ (2024) Urbanscape-
Heechan H et al (2024) Integrating machine learning for enhanced
Net: A spatial and self-attention guided deep neural network with
wildfire severity prediction: A study in the Upper Colorado River
multi scale feature extraction for urban land-use classification.
basin. Sci Total Environ. h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . s c i t o t e n v . 2 0 2 4
Conference: IGARSS 2024 - 2024 IEEE International Geosci-
. 1 7 5 9 1 4
ence and Remote Sensing Symposium. h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / i
Hernandez-Sequeira I, Fernandez-Beltran R, Pla F (2022) Transfer
g a r s s 5 3 4 7 5 . 2 0 2 4 . 1 0 6 4 0 9 6 5
deep learning for remote sensing datasets: a comparison study,"
Chuanming Z (2024) Enhancing climate monitoring and prediction:
IGARSS 2022 - 2022 IEEE International Geoscience and Remote
The integration of advanced AI techniques. Appl Computational
Sensing Symposium, Kuala Lumpur, Malaysia, 2022, pp. 3207–
Eng. h t t p s : / / d oi . o r g / 1 0 . 5 4 2 5 4 / 2 7 5 5 - 2 7 2 1 / 7 1 / 2 0 2 4 1 5 8 3
3210. h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / I G A R S S 4 6 8 3 4 . 2 0 2 2 . 9 8 8 4 6 6 7
Danqing Xu, Yiquan Wu (2023) An efficient detector with auxiliary
Hewarathna AI et al. (2024) Change detection for forest ecosystems
network for remote sensing object detection. Electronics. h t t p s : / /
using remote sensing images with siamese attention U-Net. Tech-
d o i . o r g / 1 0 . 3 3 9 0 / e l e c t r o n i c s 1 2 2 1 4 4 4 8
nologies (Basel), h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / t e c h n o l o g i e s 1 2 0 9 0 1 6 0
Devi KLSR, Kumar GN, Narayana PA, Ramana KV, Amarendra K,
Hou T, Jing Li (2024) Application of mask R-CNN for building detec-
Gullipalli TR Forest Fire Prediction and Management using
tion in UAV remote sensing images. Heliyon. h t t p s : / / d oi . o r g / 1 0 . 1
AI (Artificial Intelligence), ML (Machine Learning) and Deep
0 1 6 / j . h e l i y o n . 2 0 2 4 . e 3 8 1 4 1
Learning Techniques, 2024 8th International Conference on
Ilmak D, Iban MC, Şeker DZ (2024) Deep learning-based scene
Inventive Systems and Control (ICISC), Coimbatore, India, 2024,
classification of very high-resolution satellite imagery for
pp. 324–327, h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / I C I S C 6 2 6 2 4 . 2 0 2 4 . 0 0 0 6 2
post-earthquake damage assessment: a case study of the 2023
Di Teodoro G, Monaci M, Palagi L (2023) Unboxing Tree Ensembles
kahramanmaraş earthquakes. The international archives of the
for interpretability: a hierarchical visualization tool and a mul-
photogrammetry, remote sensing and spatial information sci-
tivariate optimal re-built tree. EURO journal on computational
ences, h t t p s : / / d o i . o r g / 1 0 . 5 1 9 4 / i s p r s - a r c h i v e s - x l v i i i - 4 - w 9 - 2 0 2 4 - 2
optimization, h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . e j c o . 2 0 2 4 . 1 0 0 0 8 4
4 9 - 2 0 2 4
Duangkhwan W (2025). Deep learning-based flood inundation predic-
Jamunadevi C, Naveen N, Manimaran M, Janani M (2024) Applica-
tion in the pattani river basin. Int J Geomate 28(125)
tion of deep learning algorithm for prediction of flood severity.
Else S, Sindy S, Charlotte W, Boud V, Dieter W (2022) Harmoniza-
Conference: 2024 2nd International Conference on Sustainable
tion of multi-mission high-resolution time series: application to
Computing and Smart Systems (ICSCSS). h t t p s : / / d o i . o r g / 1 0 . 1 1 0
BELAIR. Remote Sens. h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / r s 1 4 0 5 1 1 6 3
9 / i c s c s s 6 0 6 6 0 . 2 0 2 4 . 1 0 6 2 5 0 2 5
Feng L, Yuan et al. (2024). Adaptive multi-source domain collabora-
Jayanth S et al (2024) Self-supervised learning across the spectrum.
tive fine-tuning for transfer learning. PeerJ. h t t p s : / / d o i . o r g / 1 0 . 7 7
Remote Sens. h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / r s 1 6 1 8 3 4 7 0
1 7 / p e e r j - c s . 2 1 0 7
Joshi DD, Kumar S, Patil S, Kamat P, Kolhar S, Kotecha K (2024)
Ferrario DM, Tiggeloven T, Casagrande S, Sanò M, de Ruiter M, Critto
Deep learning with ensemble approach for early pile fire detection
A, Torresan S (2025) An AI approach for multi-risk assessment in
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 9**


Environmental Earth Sciences (2026) 85:78 Page 9 of 10 78
using aerial images. Front Environ Sci 12:1440396. h t t p s : / / d o i . o r amazon using Landsat data and convolutional neural networks.
g / 1 0 . 3 3 8 9 / f e n v s . 2 0 2 4 . 1 4 4 0 3 9 6 Remote Sens 12(6):901
Karin M et al (2024) Macrophenological dynamics from citizen sci- Qi He, Zihang Z, Danfeng Z, Wei S, Dongmei H (2024) An Interpre-
ence plant occurrence data. Methods Ecol Evol. h t t p s : / / d o i . o r g / 1 table deep learning approach for detecting marine heatwaves pat-
0 . 1 1 1 1 / 2 0 4 1 - 2 1 0 x . 1 4 3 6 5 terns. Appl Sci. h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / a p p 1 4 0 2 0 6 0 1
Maideen AK, Nawaz SM, Basha VA, Basha A (2024) Effective utili- Rajasekhar M (2024) Understanding YOLO: real-time object detec-
sation of AI to improve global warming mitigation strategies tion explained. Interantional J Sci Res Eng Manage. h t t p s : / / d o i . o
through predictive climate modelling. Int J Data Inform Intell r g / 1 0 . 5 5 0 4 1 / i j s r e m 3 6 3 5 9
Comput h t t p s : / / d o i . o r g / 1 0 . 5 9 4 6 1 / i j d i i c . v 3 i 3 . 1 2 9 Raman V, Sumari P, Prabhavathy M, Perumal S (2024) Identification
Liu S, Wang B (2024) Optimized Modified ResNet18: A Residual of residential and commercial area using convolutional neural
Neural Network for High Resolution, 2024 IEEE 4th Interna- network. Malaysian J Sci Health Technol. h t t p s : / / d oi . o r g / 1 0 . 3 3 1
tional Conference on Electronic Technology, Communication and 0 2 / m j o s h t . v 1 0 i 2 . 3 9 6
Information (ICETCI), Changchun, China, 2024, pp. 1–5, h t t p s : / / Rao MG et al. Categorization and Interpretation of satellite image
d o i . o r g / 1 0 . 1 1 0 9 / I C E T C I 6 1 2 2 1 . 2 0 2 4 . 1 0 5 9 4 6 7 2 scenes employing AI Approaches. 2024 International Conference
Maximilian B, Tanveer H, Niklas S, Matthias S (2024) Context mat- on Knowledge Engineering and Communication Systems (ICK-
ters: leveraging spatiotemporal metadata for semi-supervised ECS), Chikkaballapur, India, 2024, pp. 1–6, h t t p s : / / d o i . o r g / 1 0 . 1 1
learning on remote sensing images. Front Artif Intell Appl. h t t p s : 0 9 / I C K E C S 6 1 4 9 2 . 2 0 2 4 . 1 0 6 1 7 3 3 0
/ / d o i . o r g / 1 0 . 3 2 3 3 / f a i a 2 4 0 7 3 9 Rebecca K et al. (2024). Monitoring vegetation patterns and their driv-
Mengmeng Z et al (2023) Remote sensing collaborative classification ers to infer resilience: Automated detection of vegetation and
using multimodal adaptive modulation Network. IEEE Trans megaherbivores from drone imagery using deep learning. Eco-
Geosci Remote Sens. h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / t g r s . 2 0 2 4 . 3 4 5 2 6 5 0 logical Inform. h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . e c o i n f . 2 0 2 4 . 1 0 2 5 8 0
Mingyuan He, Jie Z, Yang He, Xinjie Z, Zebin G (2024) Annotated Ahmad S, ElAffendi M, Alluhaidan S, Anwar MS (2024) Deep strat-
dataset for training cloud segmentation neural networks using egy of object detection in remote sensing images. Advances in
high-resolution satellite remote sensing imagery. Remote Sens. h geospatial technologies book series, h t t p s : / / d oi . o r g / 1 0 . 4 0 1 8 / 9 7 9
t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / r s 1 6 1 9 3 6 8 2 - 8 - 3 6 9 3 - 2 9 1 3 - 9 . c h 0 0 1
Narciso GAM et al. (2024) Supervised image classification model for Sameen MI, Pradhan B, Aziz OS (2018) Classification of very high
coral bleaching detection using a bi-temporal sentinel-2 image resolution aerial photos using spectral-spatial convolutional neu-
stack. The international archives of the photogrammetry, remote ral networks. J Sensors 2018(2018):1–12
sensing and spatial information sciences, h t t p s : / / d o i . o r g / 1 0 . 5 1 9 4 / Sameer S, Priyanka S (2024) Systematic review on citizen science and
i s p r s - a r c h i v e s - x l v i i i - 4 - w 8 - 2 0 2 3 - 3 9 5 - 2 0 2 4 artificial intelligence for vector-borne diseases. Int Arch Photo-
Nayak B, Panda PK Deep hybrid model to classify satellite image gramm Remote Sens Spat Inf Sci. h t t p s : / / d o i . o r g / 1 0 . 5 1 9 4 / i s p r s - a
using vegetation indices feature set, 2024 1st International Con- r c h i v e s - x l v i i i - 4 - 2 0 2 4 - 3 9 7 - 2 0 2 4
ference on Cognitive, Green and Ubiquitous Computing (IC- Shailen M (2023) Assessing long-term impacts of disaster using pre-
CGU), Bhubaneswar, India, 2024, pp. 1–5, h t t p s : / / d o i . o r g / 1 0 . 1 1 dictive data analyticsfor effective decision support. Int J Adv Res
0 9 / I C - C G U 5 8 0 7 8 . 2 0 2 4 . 1 0 5 3 0 8 1 6 Comput Sci. h t t p s : / / d o i . o r g / 1 0 . 2 6 4 8 3 / i j a r c s . v 1 4 i 2 . 6 9 5 6
Nicole W et al (2024) There is a need to better take into account forest Shi J, Lv D, Chen T, Li Y (2024) Learning-based inter-satellite com-
soils in the planned soil monitoring law of the European Union. putation offloading in satellite edge computing. Conference: 2024
Ann Sci. h t t p s : / / d o i . o r g / 1 0 . 1 1 8 6 / s 1 3 5 9 5 - 0 2 4 - 0 1 2 3 8 - 7 9th International Conference on Signal and Image Processing
Nzeanorue CG et al. (2024) Advanced remote sensing technologies for (ICSIP). h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / i c s i p 6 1 8 8 1 . 2 0 2 4 . 1 0 6 7 1 5 1 0
tracking landscape changes and environmental conditions. World Shrestha S, Dahal D, Bhattarai N, Regmi SM, Sewa R, Kalra A (2025)
J Adv Res Rev h t t p s : / / d o i . o r g / 1 0 . 3 0 5 7 4 / w j a r r . 2 0 2 4 . 2 3 . 1 . 2 0 5 7 Machine learning-based flood risk assessment in urban water-
Oku, Krishnamurthy., Laxmi, Srinivas, Samayamantri., Sangeeta, shed: mapping flood susceptibility in Charlotte, North Carolina.
Singhal., R., Steffi. (2024). Decoding AI Decisions on Depth Map Geographies 5(3):43
Analysis for Enhanced Interpretability. Advances in computer Shu-Wei Fu, Meng-Chieh F, Po-Wei C, Tzung-Su D (2024) Combin-
and electrical engineering book series. h t t p s : / / d o i . o r g / 1 0 . 4 0 1 8 / 9 ing citizen science data and literature to build a traits dataset of
7 9 - 8 - 3 6 9 3 - 3 7 3 9 - 4 . c h 0 0 8. Taiwan’s birds. Sci Data. h t t p s : / / d o i . o r g / 1 0 . 1 0 3 8 / s 4 1 5 9 7 - 0 2 4 - 0 3
Padilla-Arballo JJ, Martínez-Díaz S, Castro-Liera MA, Luna-Taylor 9 2 8 - 3
JE (2022) Detección de cambio en superficie costera mediante Stefanos G et al (2024) Storm surge modeling in the AI era: Using
la segmentación de imágenes aéreas utilizando redes neuronales LSTM-based machine learning for enhancing forecasting accu-
convolucionales. PÄDI Boletín Científico De Ciencias Básicas e racy. Coast Eng. h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . c o a s t a l e n g . 2 0 2 4 . 1 0 4 5
Ingenierías Del ICBI 10(Especial4):136–144 3 2
Paiano M, Lenoir P, Giannelli C, Filippo C (2024) Transfer learning Sudiana D, Putri SH, Kushardono D, Prabuwono AS, Sumantyo JTS,
with generative models for object detection on limited datasets. Rizkinia M (2025) CNN-random forest hybrid method for phe-
Mach Learn: science and technology, h t t p s : / / d o i . o r g / 1 0 . 1 0 8 8 / 2 6 nology-based paddy rice mapping using Sentinel-2 and Landsat-8
3 2 - 2 1 5 3 / a d 6 5 b 5 satellite images. Computers 14(8):336
Pinder N et al. (2024) Predicting snow water equivalent in the Surbhi M et al (2024) On responsible machine learning datasets
Tuolumne River Basin, CA Through Time Series Forecasting emphasizing fairness, privacy and regulatory norms with exam-
Using Deep-Learning," IGARSS 2024 - 2024 IEEE International ples in biometrics and healthcare. Nature MachIntell. h t t p s : / / d o i .
Geoscience and Remote Sensing Symposium, Athens, Greece, o r g / 1 0 . 1 0 3 8 / s 4 2 2 5 6 - 0 2 4 - 0 0 8 7 4 - y
2024, pp. 1859–1863, h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / I G A R S S 5 3 4 7 5 . 2 0 Tachasit C, Akadej U, Sarun I (2024) Comparative analysis of deep
2 4 . 1 0 6 4 0 8 3 5 learning models for building extraction from high-resolution sat-
Potić I et al (2023) Improving forest detection using machine learning ellite imagery. Curr Appl Sci Technol. h t t p s : / / d o i . o r g / 1 0 . 5 5 0 0 3 / c
and remote sensing: a case study in Southeastern Serbia. Appl Sci. a s t . 2 0 2 4 . 2 6 0 8 4 6
h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / a p p 1 3 1 48 2 8 9 Tepetidis N, Benekos I, Iliopoulou T, Dimitriadis P, Koutsoyiannis D
Pozzobon de Bem P, de Carvalho Júnior OA, Guimarães RF, Gomes (2025) Combining machine learning models and satellite data of
RAT (2020) Change detection of deforestation in the Brazilian
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 10**


78 Page 10 of 10 Environmental Earth Sciences (2026) 85:78
an extreme flood event for flood susceptibility mapping. Water Zambre Y, Rajkitkul E, Mohan A, Peeples J (2024) Spatial transformer
17(18):2678 network YOLO Model for Agricultural Object Detection. arXiv.
Tufail R, Tassinari P, Torreggiani D (2025) Deep learning applications org, h t t p s : / / d o i . o r g / 1 0 . 4 8 5 5 0 / a r x i v . 2 4 0 7 . 2 1 6 5 2
for crop mapping using multi-temporal Sentinel-2 data and red- Zangana HM, Mustafa FM, Omar M (2024) A hybrid approach for
edge vegetation indices: integrating convolutional and recurrent robust object detection: integrating template matching and faster
neural networks. Remote Sens 17(18):3207 R-CNN. EAI endorsed transactions on artificial intelligence and
Vaka DS, Yaragunda VR, Perdikou S, Papanicolaou AN (2024) InSAR robotics, h t t p s : / / d o i . o r g / 1 0 . 4 1 0 8 / a i r o . 6 8 5 8
Integrated Machine Learning Approach for Landslide Suscepti- Zhipeng Lü (2024) Image feature selection based on attention mecha-
bility Mapping in California. Remote sensing, h t t p s : / / d o i . o r g / 1 0 nism. Acad J Sci Technol. h t t p s : / / d o i . o r g / 1 0 . 5 4 0 9 7 / 9 m z 6 8 c 7 8
. 3 3 9 0 / r s 1 6 1 9 3 5 7 4 Zhipeng C et al (2023) A large scale training sample database system
Vaughan A et al. (2024) AI for operational methane emitter monitoring for intelligent interpretation of remote sensing imagery. Geo-
from space. arXiv:2408.04745. h t t p s : / / d o i . o r g / 1 0 . 4 8 5 5 0 / a r x i v . 2 4 Spatial Information Science. h t t p s : / / d oi . o r g / 1 0 . 1 0 8 0 / 1 0 0 9 5 0 2 0 .
0 8 . 0 4 7 4 5 2 0 2 3 . 2 2 4 4 0 0 5
Wenqing F, Fangli G, Chenhao S, Wei Xu (2024) Feature-differencing- Zhonghua He et al (2024) Spatio-temporal modeling of satellite-
based self-supervised pre-training for land-use/land-cover change observed CO2 columns in China using deep learning. Int J Appl
detection in high-resolution remote sensing images. Land. h t t p s : / Earth Obs Geoinf. h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . j a g . 2 0 2 4 . 1 0 3 8 5 9
/ d o i . o r g / 1 0 . 3 3 9 0 / l a n d 1 3 0 7 0 9 2 7 Zhujun Gu, Maimai Z (2023) The use of artificial intelligence and sat-
Xizhen Z et al (2024) Deep multi-order spatial-spectral residual fea- ellite remote sensing in land cover change detection: review and
ture extractor for weak information mining in remote sensing perspectives. Sustainability. h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / s u 1 6 0 1 0 2 7 4
imagery. Remote Sens. h t t p s : / / d o i . o r g / 1 0 . 3 3 9 0 / r s 1 6 1 1 1 9 5 7
Yuan Y, Yangfan Z, Zhi-Peng X (2023) Parameter-efficient transfer Publisher's Note Springer Nature remains neutral with regard to juris-
learning for remote sensing image-text retrieval. IEEE Trans dictional claims in published maps and institutional affiliations.
Geosci Remote Sens. h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / t g r s . 2 0 2 3 . 3 3 0 8 9 6 9
1 3
Content courtesy of Springer Nature, terms of use apply. Rights reserved.


---

**Page 11**


Terms and Conditions
S pringer Nature journal content, brought to you courtesy of Springer Nature Customer Service Center GmbH (“Springer Nature”).
Springer Nature supports a reasonable amount of sharing of research papers by authors, subscribers and authorised users (“Users”), for small-
scale personal, non-commercial use provided that all copyright, trade and service marks and other proprietary notices are maintained. By
accessing, sharing, receiving or otherwise using the Springer Nature journal content you agree to these terms of use (“Terms”). For these
p urposes, Springer Nature considers academic use (by researchers and students) to be non-commercial.
These Terms are supplementary and will apply in addition to any applicable website terms and conditions, a relevant site licence or a personal
subscription. These Terms will prevail over any conflict or ambiguity with regards to the relevant terms, a site licence or a personal subscription
(to the extent of the conflict or ambiguity only). For Creative Commons-licensed articles, the terms of the Creative Commons license used will
a pply.
We collect and use personal data to provide access to the Springer Nature journal content. We may also use these personal data internally within
ResearchGate and Springer Nature and as agreed share it, in an anonymised way, for purposes of tracking, analysis and reporting. We will not
otherwise disclose your personal data outside the ResearchGate or the Springer Nature group of companies unless we have your permission as
d etailed in the Privacy Policy.
While Users may use the Springer Nature journal content for small scale, personal non-commercial use, it is important to note that Users may
n ot:
1.use such content for the purpose of providing other users with access on a regular or large scale basis or as a means to circumvent access
control;
2.use such content where to do so would be considered a criminal or statutory offence in any jurisdiction, or gives rise to civil liability, or is
otherwise unlawful;
3.falsely or misleadingly imply or suggest endorsement, approval , sponsorship, or association unless explicitly agreed to by Springer Nature in
writing;
4.use bots or other automated methods to access the content or redirect messages
5.override any security feature or exclusionary protocol; or
6.share the content in order to create substitute for Springer Nature products or services or a systematic database of Springer Nature journal
content.
In line with the restriction against commercial use, Springer Nature does not permit the creation of a product or service that creates revenue,
royalties, rent or income from our content or its inclusion as part of a paid for service or for other commercial gain. Springer Nature journal
content cannot be used for inter-library loans and librarians may not upload Springer Nature journal content on a large scale into their, or any
o ther, institutional repository.
These terms of use are reviewed regularly and may be amended at any time. Springer Nature is not obligated to publish any information or
content on this website and may remove it or features or functionality at our sole discretion, at any time with or without notice. Springer Nature
m ay revoke this licence to you at any time and remove access to any copies of the Springer Nature journal content which have been saved.
To the fullest extent permitted by law, Springer Nature makes no warranties, representations or guarantees to Users, either express or implied
with respect to the Springer nature journal content and all parties disclaim and waive any implied warranties or warranties imposed by law,
i ncluding merchantability or fitness for any particular purpose.
Please note that these rights do not automatically extend to content, data or other material published by Springer Nature that may be licensed
f rom third parties.
If you would like to use or distribute our Springer Nature journal content to a wider audience or on a regular basis or in any other manner not
e xpressly permitted by these Terms, please contact Springer Nature at
onlineservice@springernature.com
