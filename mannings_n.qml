<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Symbology3D|Labeling|Fields|Forms|Actions|Diagrams|GeometryOptions|Relations|Legend" version="3.40.1-Bratislava">
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option name="name" type="QString" value=""/>
      <Option name="properties"/>
      <Option name="type" type="QString" value="collection"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" classificationMin="0.01" opacity="1" band="1" alphaBand="-1" classificationMax="0.25">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader labelPrecision="0" classificationMode="1" minimumValue="0.01" maximumValue="0.25" colorRampType="INTERPOLATED" clip="0">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option name="color1" type="QString" value="68,1,84,255,rgb:0.26666666666666666,0.00392156862745098,0.32941176470588235,1"/>
              <Option name="color2" type="QString" value="253,231,37,255,rgb:0.99215686274509807,0.90588235294117647,0.14509803921568629,1"/>
              <Option name="direction" type="QString" value="ccw"/>
              <Option name="discrete" type="QString" value="0"/>
              <Option name="rampType" type="QString" value="gradient"/>
              <Option name="spec" type="QString" value="rgb"/>
              <Option name="stops" type="QString" value="0.019608;70,8,92,255,rgb:0.27450980392156865,0.03137254901960784,0.36078431372549019,1;rgb;ccw:0.039216;71,16,99,255,rgb:0.27843137254901962,0.06274509803921569,0.38823529411764707,1;rgb;ccw:0.058824;72,23,105,255,rgb:0.28235294117647058,0.09019607843137255,0.41176470588235292,1;rgb;ccw:0.078431;72,29,111,255,rgb:0.28235294117647058,0.11372549019607843,0.43529411764705883,1;rgb;ccw:0.098039;72,36,117,255,rgb:0.28235294117647058,0.14117647058823529,0.45882352941176469,1;rgb;ccw:0.117647;71,42,122,255,rgb:0.27843137254901962,0.16470588235294117,0.47843137254901963,1;rgb;ccw:0.137255;70,48,126,255,rgb:0.27450980392156865,0.18823529411764706,0.49411764705882355,1;rgb;ccw:0.156863;69,55,129,255,rgb:0.27058823529411763,0.21568627450980393,0.50588235294117645,1;rgb;ccw:0.176471;67,61,132,255,rgb:0.2627450980392157,0.23921568627450981,0.51764705882352946,1;rgb;ccw:0.196078;65,66,135,255,rgb:0.25490196078431371,0.25882352941176473,0.52941176470588236,1;rgb;ccw:0.215686;63,72,137,255,rgb:0.24705882352941178,0.28235294117647058,0.53725490196078429,1;rgb;ccw:0.235294;61,78,138,255,rgb:0.23921568627450981,0.30588235294117649,0.54117647058823526,1;rgb;ccw:0.254902;58,83,139,255,rgb:0.22745098039215686,0.32549019607843138,0.54509803921568623,1;rgb;ccw:0.27451;56,89,140,255,rgb:0.2196078431372549,0.34901960784313724,0.5490196078431373,1;rgb;ccw:0.294118;53,94,141,255,rgb:0.20784313725490197,0.36862745098039218,0.55294117647058827,1;rgb;ccw:0.313725;51,99,141,255,rgb:0.20000000000000001,0.38823529411764707,0.55294117647058827,1;rgb;ccw:0.333333;49,104,142,255,rgb:0.19215686274509805,0.40784313725490196,0.55686274509803924,1;rgb;ccw:0.352941;46,109,142,255,rgb:0.1803921568627451,0.42745098039215684,0.55686274509803924,1;rgb;ccw:0.372549;44,113,142,255,rgb:0.17254901960784313,0.44313725490196076,0.55686274509803924,1;rgb;ccw:0.392157;42,118,142,255,rgb:0.16470588235294117,0.46274509803921571,0.55686274509803924,1;rgb;ccw:0.411765;41,123,142,255,rgb:0.16078431372549021,0.4823529411764706,0.55686274509803924,1;rgb;ccw:0.431373;39,128,142,255,rgb:0.15294117647058825,0.50196078431372548,0.55686274509803924,1;rgb;ccw:0.45098;37,132,142,255,rgb:0.14509803921568629,0.51764705882352946,0.55686274509803924,1;rgb;ccw:0.470588;35,137,142,255,rgb:0.13725490196078433,0.53725490196078429,0.55686274509803924,1;rgb;ccw:0.490196;33,142,141,255,rgb:0.12941176470588237,0.55686274509803924,0.55294117647058827,1;rgb;ccw:0.509804;32,146,140,255,rgb:0.12549019607843137,0.5725490196078431,0.5490196078431373,1;rgb;ccw:0.529412;31,151,139,255,rgb:0.12156862745098039,0.59215686274509804,0.54509803921568623,1;rgb;ccw:0.54902;30,156,137,255,rgb:0.11764705882352941,0.61176470588235299,0.53725490196078429,1;rgb;ccw:0.568627;31,161,136,255,rgb:0.12156862745098039,0.63137254901960782,0.53333333333333333,1;rgb;ccw:0.588235;33,165,133,255,rgb:0.12941176470588237,0.6470588235294118,0.52156862745098043,1;rgb;ccw:0.607843;36,170,131,255,rgb:0.14117647058823529,0.66666666666666663,0.51372549019607838,1;rgb;ccw:0.627451;40,174,128,255,rgb:0.15686274509803921,0.68235294117647061,0.50196078431372548,1;rgb;ccw:0.647059;46,179,124,255,rgb:0.1803921568627451,0.70196078431372544,0.48627450980392156,1;rgb;ccw:0.666667;53,183,121,255,rgb:0.20784313725490197,0.71764705882352942,0.47450980392156861,1;rgb;ccw:0.686275;61,188,116,255,rgb:0.23921568627450981,0.73725490196078436,0.45490196078431372,1;rgb;ccw:0.705882;70,192,111,255,rgb:0.27450980392156865,0.75294117647058822,0.43529411764705883,1;rgb;ccw:0.72549;80,196,106,255,rgb:0.31372549019607843,0.7686274509803922,0.41568627450980394,1;rgb;ccw:0.745098;90,200,100,255,rgb:0.35294117647058826,0.78431372549019607,0.39215686274509803,1;rgb;ccw:0.764706;101,203,94,255,rgb:0.396078431372549,0.79607843137254897,0.36862745098039218,1;rgb;ccw:0.784314;112,207,87,255,rgb:0.4392156862745098,0.81176470588235294,0.3411764705882353,1;rgb;ccw:0.803922;124,210,80,255,rgb:0.48627450980392156,0.82352941176470584,0.31372549019607843,1;rgb;ccw:0.823529;137,213,72,255,rgb:0.53725490196078429,0.83529411764705885,0.28235294117647058,1;rgb;ccw:0.843137;149,216,64,255,rgb:0.58431372549019611,0.84705882352941175,0.25098039215686274,1;rgb;ccw:0.862745;162,218,55,255,rgb:0.63529411764705879,0.85490196078431369,0.21568627450980393,1;rgb;ccw:0.882353;176,221,47,255,rgb:0.69019607843137254,0.8666666666666667,0.18431372549019609,1;rgb;ccw:0.901961;189,223,38,255,rgb:0.74117647058823533,0.87450980392156863,0.14901960784313725,1;rgb;ccw:0.921569;202,225,31,255,rgb:0.792156862745098,0.88235294117647056,0.12156862745098039,1;rgb;ccw:0.941176;216,226,25,255,rgb:0.84705882352941175,0.88627450980392153,0.09803921568627451,1;rgb;ccw:0.960784;229,228,25,255,rgb:0.89803921568627454,0.89411764705882357,0.09803921568627451,1;rgb;ccw:0.980392;241,229,29,255,rgb:0.94509803921568625,0.89803921568627454,0.11372549019607843,1;rgb;ccw"/>
            </Option>
          </colorramp>
          <item label="0" value="0.01" alpha="255" color="#440154"/>
          <item label="0" value="0.014705872" alpha="255" color="#46085c"/>
          <item label="0" value="0.019411768" alpha="255" color="#471063"/>
          <item label="0" value="0.02411764" alpha="255" color="#481769"/>
          <item label="0" value="0.028823536" alpha="255" color="#481d6f"/>
          <item label="0" value="0.033529408" alpha="255" color="#482475"/>
          <item label="0" value="0.03823528" alpha="255" color="#472a7a"/>
          <item label="0" value="0.0429412" alpha="255" color="#46307e"/>
          <item label="0" value="0.04764712" alpha="255" color="#453781"/>
          <item label="0" value="0.05235304" alpha="255" color="#433d84"/>
          <item label="0" value="0.05705872" alpha="255" color="#414287"/>
          <item label="0" value="0.06176464" alpha="255" color="#3f4889"/>
          <item label="0" value="0.06647056" alpha="255" color="#3d4e8a"/>
          <item label="0" value="0.07117648" alpha="255" color="#3a538b"/>
          <item label="0" value="0.0758824" alpha="255" color="#38598c"/>
          <item label="0" value="0.08058832" alpha="255" color="#355e8d"/>
          <item label="0" value="0.085294" alpha="255" color="#33638d"/>
          <item label="0" value="0.08999992" alpha="255" color="#31688e"/>
          <item label="0" value="0.09470584" alpha="255" color="#2e6d8e"/>
          <item label="0" value="0.09941176" alpha="255" color="#2c718e"/>
          <item label="0" value="0.10411768" alpha="255" color="#2a768e"/>
          <item label="0" value="0.1088236" alpha="255" color="#297b8e"/>
          <item label="0" value="0.11352952" alpha="255" color="#27808e"/>
          <item label="0" value="0.1182352" alpha="255" color="#25848e"/>
          <item label="0" value="0.12294112" alpha="255" color="#23898e"/>
          <item label="0" value="0.12764704" alpha="255" color="#218e8d"/>
          <item label="0" value="0.13235296" alpha="255" color="#20928c"/>
          <item label="0" value="0.13705888" alpha="255" color="#1f978b"/>
          <item label="0" value="0.1417648" alpha="255" color="#1e9c89"/>
          <item label="0" value="0.14647048" alpha="255" color="#1fa188"/>
          <item label="0" value="0.1511764" alpha="255" color="#21a585"/>
          <item label="0" value="0.15588232" alpha="255" color="#24aa83"/>
          <item label="0" value="0.16058824" alpha="255" color="#28ae80"/>
          <item label="0" value="0.16529416" alpha="255" color="#2eb37c"/>
          <item label="0" value="0.17000008" alpha="255" color="#35b779"/>
          <item label="0" value="0.174706" alpha="255" color="#3dbc74"/>
          <item label="0" value="0.17941168" alpha="255" color="#46c06f"/>
          <item label="0" value="0.1841176" alpha="255" color="#50c46a"/>
          <item label="0" value="0.18882352" alpha="255" color="#5ac864"/>
          <item label="0" value="0.19352944" alpha="255" color="#65cb5e"/>
          <item label="0" value="0.19823536" alpha="255" color="#70cf57"/>
          <item label="0" value="0.20294128" alpha="255" color="#7cd250"/>
          <item label="0" value="0.20764696" alpha="255" color="#89d548"/>
          <item label="0" value="0.21235288" alpha="255" color="#95d840"/>
          <item label="0" value="0.2170588" alpha="255" color="#a2da37"/>
          <item label="0" value="0.22176472" alpha="255" color="#b0dd2f"/>
          <item label="0" value="0.22647064" alpha="255" color="#bddf26"/>
          <item label="0" value="0.23117656" alpha="255" color="#cae11f"/>
          <item label="0" value="0.23588224" alpha="255" color="#d8e219"/>
          <item label="0" value="0.24058816" alpha="255" color="#e5e419"/>
          <item label="0" value="0.24529408" alpha="255" color="#f1e51d"/>
          <item label="0" value="0.25" alpha="255" color="#fde725"/>
          <rampLegendSettings minimumLabel="" suffix="" maximumLabel="" prefix="" useContinuousLegend="1" direction="0" orientation="2">
            <numericFormat id="basic">
              <Option type="Map">
                <Option name="decimal_separator" type="invalid"/>
                <Option name="decimals" type="int" value="6"/>
                <Option name="rounding_type" type="int" value="0"/>
                <Option name="show_plus" type="bool" value="false"/>
                <Option name="show_thousand_separator" type="bool" value="true"/>
                <Option name="show_trailing_zeros" type="bool" value="false"/>
                <Option name="thousand_separator" type="invalid"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" gamma="1" brightness="0"/>
    <huesaturation colorizeRed="255" colorizeStrength="100" colorizeOn="0" grayscaleMode="0" colorizeBlue="128" saturation="0" colorizeGreen="128" invertColors="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
