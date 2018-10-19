%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%ParseJAADBehXML.m          %
%Author: Liu Yang           %
%Mail: liuyeung@stanford.edu%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [behAnn] = ParseJAADBehXML(behaviorXMLPath) 
  fileList = dir(fullfile(behaviorXMLPath));
  fileNum = length(fileList);
  behAnn = containers.Map;
  for i = 1:fileNum
      if(fileList(i).isdir == 0)
          fileName = fileList(i).name;
          if(~isempty(regexp(fileName, '.*\.xml', 'match')))
              xmlPath = fullfile(behaviorXMLPath, fileName);
              xmlDoc = xml2struct(xmlPath);
              pedAct = ParsePedAct(xmlDoc);
              seg = split(fileName, '.');
              behAnn(seg{1}) = pedAct;
          end
      end
  end
end