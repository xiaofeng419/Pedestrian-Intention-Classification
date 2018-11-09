%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%GenerateAnnotatedData.m       %
%Author: Liu Yang              %
%Mail: liuyeung@stanford.edu   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

vbbRoot = '../../Dataset/JAAD_pedestrian/vbb_part';
seqRoot = '../../Dataset/JAAD_videos';
sampleRoot = '../../Dataset/Data_by_Matlab';
behaviorXMLPath = '../../Dataset/JAAD_behavior/behavioral_data_xml';

attAnn = ParseJAADBehAnnote('./pedestrian_behavior_attributes.txt');
behAnn = ParseJAADBehXML(behaviorXMLPath);
%SampleCrossData(attAnn, behAnn, vbbRoot, seqRoot, sampleRoot);
SampleNonCrossData(attAnn, behAnn, vbbRoot,j seqRoot, sampleRoot);