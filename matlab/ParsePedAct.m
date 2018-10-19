%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%ParsePedAct.m              %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [pedAct] = ParsePedAct(xmlInfo)
  peds = fieldnames(xmlInfo.video.actions);
  peds = regexp(peds, 'pedestrian.*', 'match'); %filter the pedestrian out
  indx = find(cellfun(@length, peds) > 0);
  pedAct = struct();
  for i = 1:length(indx)
     idx = indx(i); 
     xmlPed = xmlInfo.video.actions.(peds{idx}{1});
     actNum = length(xmlPed.action);
     act = cell(1, actNum);
     if(actNum > 1)
         for j = 1:actNum
             act{j} = convertActField(xmlPed.action{j}.Attributes);
         end
     else
         act{1} = convertActField(xmlPed.action.Attributes);
     end
     pedAct.(peds{idx}{1}) = cell2mat(act);
  end
end

function [ret] = convertActField(attribute)
   ret = struct();
   ret.end_frame = str2double(attribute.end_frame);
   ret.end_time = str2double(attribute.end_time);
   ret.id = attribute.id;
   ret.start_frame = str2double(attribute.start_frame);
   ret.start_time = str2double(attribute.start_time);
end