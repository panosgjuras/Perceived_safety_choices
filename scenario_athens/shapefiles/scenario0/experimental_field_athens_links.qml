<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.20.2-Odense" simplifyDrawingTol="1" simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" styleCategories="AllStyleCategories" labelsEnabled="0" simplifyAlgorithm="0" maxScale="0" minScale="100000000" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" endField="" fixedDuration="0" startField="" endExpression="" startExpression="" durationField="id" durationUnit="min" accumulate="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="categorizedSymbol" symbollevels="0" attr="inf" enableorderby="0" forceraster="0">
    <categories>
      <category label="1: Urban road with sidewalk less than 1.5 m wide" render="true" value="1: Urban road with sidewalk less than 1.5 m wide" symbol="0"/>
      <category label="2: Urban road with sidewalk more than 1.5 m wide" render="true" value="2: Urban road with sidewalk more than 1.5 m wide" symbol="1"/>
      <category label="3: Urban road with cycle lane" render="true" value="3: Urban road with cycle lane" symbol="2"/>
      <category label="4: Shared space" render="true" value="4: Shared space" symbol="3"/>
    </categories>
    <symbols>
      <symbol type="line" force_rhr="0" name="0" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="square"/>
            <Option type="QString" name="customdash" value="5;2"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="line_color" value="227,26,28,255"/>
            <Option type="QString" name="line_style" value="solid"/>
            <Option type="QString" name="line_width" value="0.75"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="0"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="227,26,28,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.75"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="field" value="pav"/>
                  <Option type="int" name="type" value="2"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" force_rhr="0" name="1" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="square"/>
            <Option type="QString" name="customdash" value="5;2"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="line_color" value="255,127,0,255"/>
            <Option type="QString" name="line_style" value="solid"/>
            <Option type="QString" name="line_width" value="0.75"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="0"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,127,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.75"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" force_rhr="0" name="2" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="square"/>
            <Option type="QString" name="customdash" value="5;2"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="line_color" value="0,0,255,255"/>
            <Option type="QString" name="line_style" value="solid"/>
            <Option type="QString" name="line_width" value="0.75"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="0"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="0,0,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.75"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="line" force_rhr="0" name="3" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="square"/>
            <Option type="QString" name="customdash" value="5;2"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="line_color" value="29,208,131,255"/>
            <Option type="QString" name="line_style" value="solid"/>
            <Option type="QString" name="line_width" value="0.75"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="0"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="29,208,131,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.75"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol type="line" force_rhr="0" name="0" alpha="1" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </data_defined_properties>
        <layer locked="0" enabled="1" class="SimpleLine" pass="0">
          <Option type="Map">
            <Option type="QString" name="align_dash_pattern" value="0"/>
            <Option type="QString" name="capstyle" value="square"/>
            <Option type="QString" name="customdash" value="5;2"/>
            <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="customdash_unit" value="MM"/>
            <Option type="QString" name="dash_pattern_offset" value="0"/>
            <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
            <Option type="QString" name="draw_inside_polygon" value="0"/>
            <Option type="QString" name="joinstyle" value="bevel"/>
            <Option type="QString" name="line_color" value="0,0,183,255"/>
            <Option type="QString" name="line_style" value="solid"/>
            <Option type="QString" name="line_width" value="0.75"/>
            <Option type="QString" name="line_width_unit" value="MM"/>
            <Option type="QString" name="offset" value="0"/>
            <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="offset_unit" value="MM"/>
            <Option type="QString" name="ring_filter" value="0"/>
            <Option type="QString" name="trim_distance_end" value="0"/>
            <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_end_unit" value="MM"/>
            <Option type="QString" name="trim_distance_start" value="0"/>
            <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            <Option type="QString" name="trim_distance_start_unit" value="MM"/>
            <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
            <Option type="QString" name="use_custom_dash" value="0"/>
            <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
          </Option>
          <prop k="align_dash_pattern" v="0"/>
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="dash_pattern_offset" v="0"/>
          <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="dash_pattern_offset_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="0,0,183,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.75"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="trim_distance_end" v="0"/>
          <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_end_unit" v="MM"/>
          <prop k="trim_distance_start" v="0"/>
          <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="trim_distance_start_unit" v="MM"/>
          <prop k="tweak_dash_pattern_on_corners" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style legendString="Aa" fontWordSpacing="0" allowHtml="0" previewBkgrdColor="255,255,255,255" fontFamily="Arial" multilineHeight="1" fontSize="6" fontUnderline="0" textOpacity="1" fieldName="id" capitalization="0" fontItalic="0" blendMode="0" fontStrikeout="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontKerning="1" fontLetterSpacing="0" fontWeight="50" textColor="227,26,28,255" useSubstitutions="0" fontSizeUnit="Point" namedStyle="????????" isExpression="0" textOrientation="horizontal">
        <families/>
        <text-buffer bufferNoFill="1" bufferJoinStyle="128" bufferSizeUnits="MM" bufferOpacity="1" bufferSize="1" bufferColor="250,250,250,255" bufferBlendMode="0" bufferDraw="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <text-mask maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskType="0" maskJoinStyle="128" maskOpacity="1" maskedSymbolLayers="" maskSizeUnits="MM" maskEnabled="0" maskSize="0"/>
        <background shapeJoinStyle="64" shapeFillColor="255,255,255,255" shapeOffsetUnit="Point" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeBorderWidth="0" shapeRadiiX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="Point" shapeType="0" shapeSizeY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeRadiiY="0" shapeSizeType="0" shapeOffsetY="0" shapeOpacity="1" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeSVGFile="" shapeBlendMode="0" shapeOffsetX="0" shapeBorderWidthUnit="Point" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeSizeUnit="Point">
          <symbol type="marker" force_rhr="0" name="markerSymbol" alpha="1" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" enabled="1" class="SimpleMarker" pass="0">
              <Option type="Map">
                <Option type="QString" name="angle" value="0"/>
                <Option type="QString" name="cap_style" value="square"/>
                <Option type="QString" name="color" value="133,182,111,255"/>
                <Option type="QString" name="horizontal_anchor_point" value="1"/>
                <Option type="QString" name="joinstyle" value="bevel"/>
                <Option type="QString" name="name" value="circle"/>
                <Option type="QString" name="offset" value="0,0"/>
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="offset_unit" value="MM"/>
                <Option type="QString" name="outline_color" value="35,35,35,255"/>
                <Option type="QString" name="outline_style" value="solid"/>
                <Option type="QString" name="outline_width" value="0"/>
                <Option type="QString" name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="outline_width_unit" value="MM"/>
                <Option type="QString" name="scale_method" value="diameter"/>
                <Option type="QString" name="size" value="2"/>
                <Option type="QString" name="size_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="size_unit" value="MM"/>
                <Option type="QString" name="vertical_anchor_point" value="1"/>
              </Option>
              <prop k="angle" v="0"/>
              <prop k="cap_style" v="square"/>
              <prop k="color" v="133,182,111,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol type="fill" force_rhr="0" name="fillSymbol" alpha="1" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
            <layer locked="0" enabled="1" class="SimpleFill" pass="0">
              <Option type="Map">
                <Option type="QString" name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="color" value="255,255,255,255"/>
                <Option type="QString" name="joinstyle" value="bevel"/>
                <Option type="QString" name="offset" value="0,0"/>
                <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
                <Option type="QString" name="offset_unit" value="MM"/>
                <Option type="QString" name="outline_color" value="128,128,128,255"/>
                <Option type="QString" name="outline_style" value="no"/>
                <Option type="QString" name="outline_width" value="0"/>
                <Option type="QString" name="outline_width_unit" value="Point"/>
                <Option type="QString" name="style" value="solid"/>
              </Option>
              <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="255,255,255,255"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="128,128,128,255"/>
              <prop k="outline_style" v="no"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="Point"/>
              <prop k="style" v="solid"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowRadiusUnit="MM" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowDraw="0" shadowOpacity="0.69999999999999996" shadowBlendMode="6" shadowRadius="1.5" shadowColor="0,0,0,255" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetUnit="MM" shadowOffsetAngle="135" shadowScale="100" shadowUnder="0"/>
        <dd_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format decimals="3" placeDirectionSymbol="0" addDirectionSymbol="0" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" formatNumbers="0" wrapChar="" leftDirectionSymbol="&lt;" multilineAlign="0" autoWrapLength="0" reverseDirectionSymbol="0" plussign="0"/>
      <placement lineAnchorClipping="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" lineAnchorType="0" geometryGeneratorEnabled="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" placementFlags="10" priority="5" centroidWhole="0" yOffset="0" distUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" quadOffset="4" geometryGenerator="" geometryGeneratorType="PointGeometry" polygonPlacementFlags="2" maxCurvedCharAngleIn="25" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" repeatDistance="0" xOffset="0" dist="0" offsetUnits="MM" repeatDistanceUnits="MM" overrunDistanceUnit="MM" rotationAngle="0" layerType="LineGeometry" centroidInside="0" preserveRotation="1" maxCurvedCharAngleOut="-25" placement="2" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0"/>
      <rendering scaleMax="0" scaleMin="0" fontMaxPixelSize="10000" obstacleFactor="1" labelPerPart="0" minFeatureSize="0" maxNumLabels="2000" obstacle="1" mergeLines="0" scaleVisibility="0" upsidedownLabels="0" limitNumLabels="0" displayAll="0" unplacedVisibility="0" obstacleType="1" zIndex="0" drawLabels="1" fontLimitPixelSize="0" fontMinPixelSize="3"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" name="name" value=""/>
          <Option name="properties"/>
          <Option type="QString" name="type" value="collection"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option type="QString" name="anchorPoint" value="pole_of_inaccessibility"/>
          <Option type="int" name="blendMode" value="0"/>
          <Option type="Map" name="ddProperties">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
          <Option type="bool" name="drawToAllParts" value="false"/>
          <Option type="QString" name="enabled" value="0"/>
          <Option type="QString" name="labelAnchorPoint" value="point_on_exterior"/>
          <Option type="QString" name="lineSymbol" value="&lt;symbol type=&quot;line&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer locked=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;align_dash_pattern&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;capstyle&quot; value=&quot;square&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;customdash&quot; value=&quot;5;2&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;customdash_unit&quot; value=&quot;MM&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;dash_pattern_offset&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;draw_inside_polygon&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;joinstyle&quot; value=&quot;bevel&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;line_color&quot; value=&quot;60,60,60,255&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;line_style&quot; value=&quot;solid&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;line_width&quot; value=&quot;0.3&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;line_width_unit&quot; value=&quot;MM&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;offset&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;offset_unit&quot; value=&quot;MM&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;ring_filter&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;trim_distance_end&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;trim_distance_start&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;use_custom_dash&quot; value=&quot;0&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
          <Option type="double" name="minLength" value="0"/>
          <Option type="QString" name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="minLengthUnit" value="MM"/>
          <Option type="double" name="offsetFromAnchor" value="0"/>
          <Option type="QString" name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="offsetFromAnchorUnit" value="MM"/>
          <Option type="double" name="offsetFromLabel" value="0"/>
          <Option type="QString" name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="offsetFromLabelUnit" value="MM"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <Option type="Map">
      <Option type="List" name="dualview/previewExpressions">
        <Option type="QString" value="&quot;id&quot;"/>
      </Option>
      <Option type="int" name="embeddedWidgets/count" value="0"/>
      <Option type="bool" name="qgis2web/Interactive" value="true"/>
      <Option type="bool" name="qgis2web/Visible" value="true"/>
      <Option type="QString" name="qgis2web/popup/capacity" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/cross" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/freespeed" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/id" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/inf" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/length" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/modes" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/obst" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/oneway" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/pav" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/permlanes" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/x_end" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/x_start" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/y_end" value="inline label"/>
      <Option type="QString" name="qgis2web/popup/y_start" value="inline label"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory height="15" opacity="1" spacingUnitScale="3x:0,0,0,0,0,0" diagramOrientation="Up" direction="0" sizeType="MM" spacingUnit="MM" enabled="0" penColor="#000000" maxScaleDenominator="1e+08" backgroundAlpha="255" minScaleDenominator="0" spacing="5" scaleDependency="Area" showAxis="1" barWidth="5" scaleBasedVisibility="0" lineSizeScale="3x:0,0,0,0,0,0" width="15" lineSizeType="MM" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" backgroundColor="#ffffff" labelPlacementMethod="XHeight" rotationOffset="270" penWidth="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute color="#000000" label="" field=""/>
      <axisSymbol>
        <symbol type="line" force_rhr="0" name="" alpha="1" clip_to_extent="1">
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <layer locked="0" enabled="1" class="SimpleLine" pass="0">
            <Option type="Map">
              <Option type="QString" name="align_dash_pattern" value="0"/>
              <Option type="QString" name="capstyle" value="square"/>
              <Option type="QString" name="customdash" value="5;2"/>
              <Option type="QString" name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="customdash_unit" value="MM"/>
              <Option type="QString" name="dash_pattern_offset" value="0"/>
              <Option type="QString" name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="dash_pattern_offset_unit" value="MM"/>
              <Option type="QString" name="draw_inside_polygon" value="0"/>
              <Option type="QString" name="joinstyle" value="bevel"/>
              <Option type="QString" name="line_color" value="35,35,35,255"/>
              <Option type="QString" name="line_style" value="solid"/>
              <Option type="QString" name="line_width" value="0.26"/>
              <Option type="QString" name="line_width_unit" value="MM"/>
              <Option type="QString" name="offset" value="0"/>
              <Option type="QString" name="offset_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="offset_unit" value="MM"/>
              <Option type="QString" name="ring_filter" value="0"/>
              <Option type="QString" name="trim_distance_end" value="0"/>
              <Option type="QString" name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="trim_distance_end_unit" value="MM"/>
              <Option type="QString" name="trim_distance_start" value="0"/>
              <Option type="QString" name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0"/>
              <Option type="QString" name="trim_distance_start_unit" value="MM"/>
              <Option type="QString" name="tweak_dash_pattern_on_corners" value="0"/>
              <Option type="QString" name="use_custom_dash" value="0"/>
              <Option type="QString" name="width_map_unit_scale" value="3x:0,0,0,0,0,0"/>
            </Option>
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="trim_distance_end" v="0"/>
            <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_end_unit" v="MM"/>
            <prop k="trim_distance_start" v="0"/>
            <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_start_unit" v="MM"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" zIndex="0" linePlacementFlags="18" dist="0" placement="2" showAll="1" priority="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector" showLabelLegend="0"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="x_start" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="y_start" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="x_end" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="y_end" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="length" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="freespeed" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="15" value="15"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="30" value="30"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="40" value="40"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="50" value="50"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="60" value="60"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="70" value="70"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="permlanes" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="4" value="4"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5" value="5"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="6" value="6"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="oneway" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="0" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1" value="1"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="inf" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: Urban road with sidewalk less than 1.5 m wide" value="1: Urban road with sidewalk less than 1.5 m wide"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: Urban road with sidewalk more than 1.5 m wide" value="2: Urban road with sidewalk more than 1.5 m wide"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3: Urban road with cycle lane" value="3: Urban road with cycle lane"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="4: Shared space" value="4: Shared space"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="pav" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="0: bad condition" value="0: bad condition"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1: good condition" value="1: good condition"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="obst" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="0: yes obstacles" value="0: yes obstacles"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1: no obstacles" value="1: no obstacles"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="0: without pedestrian crossings" value="0: without pedestrian crossings"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="1: with pedestrian crossings not controlled by traffic lights" value="1: with pedestrian crossings not controlled by traffic lights"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: with pedestrian crossing controlled by traffic lights" value="2: with pedestrian crossing controlled by traffic lights"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="modes" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="car" value="car"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="bicycle" value="bicycle"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="escooter" value="escooter"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="walk" value="walk"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="car,bicycle,escooter,walk" value="car,bicycle,escooter,walk"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="bicycle,escooter,walk" value="bicycle,escooter,walk"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="id"/>
    <alias index="1" name="" field="x_start"/>
    <alias index="2" name="" field="y_start"/>
    <alias index="3" name="" field="x_end"/>
    <alias index="4" name="" field="y_end"/>
    <alias index="5" name="" field="length"/>
    <alias index="6" name="" field="capacity"/>
    <alias index="7" name="" field="freespeed"/>
    <alias index="8" name="" field="permlanes"/>
    <alias index="9" name="" field="oneway"/>
    <alias index="10" name="" field="inf"/>
    <alias index="11" name="" field="pav"/>
    <alias index="12" name="" field="obst"/>
    <alias index="13" name="" field="cross"/>
    <alias index="14" name="" field="modes"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="maximum(&quot;id&quot;) + 1" field="id"/>
    <default applyOnUpdate="0" expression="xat(0)" field="x_start"/>
    <default applyOnUpdate="0" expression="yat(0)" field="y_start"/>
    <default applyOnUpdate="0" expression="xat(-1)" field="x_end"/>
    <default applyOnUpdate="0" expression="yat(-1)" field="y_end"/>
    <default applyOnUpdate="0" expression="$length" field="length"/>
    <default applyOnUpdate="0" expression="1200" field="capacity"/>
    <default applyOnUpdate="0" expression="" field="freespeed"/>
    <default applyOnUpdate="0" expression="" field="permlanes"/>
    <default applyOnUpdate="0" expression="" field="oneway"/>
    <default applyOnUpdate="0" expression="" field="inf"/>
    <default applyOnUpdate="0" expression="" field="pav"/>
    <default applyOnUpdate="0" expression="" field="obst"/>
    <default applyOnUpdate="0" expression="" field="cross"/>
    <default applyOnUpdate="0" expression="" field="modes"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="id"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="x_start"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="y_start"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="x_end"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="y_end"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="length"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="capacity"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="freespeed"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="permlanes"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="oneway"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="inf"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="pav"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="obst"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="cross"/>
    <constraint unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0" field="modes"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="x_start"/>
    <constraint exp="" desc="" field="y_start"/>
    <constraint exp="" desc="" field="x_end"/>
    <constraint exp="" desc="" field="y_end"/>
    <constraint exp="" desc="" field="length"/>
    <constraint exp="" desc="" field="capacity"/>
    <constraint exp="" desc="" field="freespeed"/>
    <constraint exp="" desc="" field="permlanes"/>
    <constraint exp="" desc="" field="oneway"/>
    <constraint exp="" desc="" field="inf"/>
    <constraint exp="" desc="" field="pav"/>
    <constraint exp="" desc="" field="obst"/>
    <constraint exp="" desc="" field="cross"/>
    <constraint exp="" desc="" field="modes"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="&quot;id&quot;">
    <columns>
      <column type="field" hidden="0" name="id" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" hidden="0" name="x_start" width="-1"/>
      <column type="field" hidden="0" name="y_start" width="-1"/>
      <column type="field" hidden="0" name="x_end" width="-1"/>
      <column type="field" hidden="0" name="y_end" width="-1"/>
      <column type="field" hidden="0" name="length" width="-1"/>
      <column type="field" hidden="0" name="capacity" width="-1"/>
      <column type="field" hidden="0" name="freespeed" width="-1"/>
      <column type="field" hidden="0" name="permlanes" width="-1"/>
      <column type="field" hidden="0" name="oneway" width="-1"/>
      <column type="field" hidden="0" name="modes" width="-1"/>
      <column type="field" hidden="0" name="inf" width="237"/>
      <column type="field" hidden="0" name="pav" width="172"/>
      <column type="field" hidden="0" name="obst" width="-1"/>
      <column type="field" hidden="0" name="cross" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="capacity"/>
    <field editable="1" name="cross"/>
    <field editable="1" name="csv expe_1"/>
    <field editable="1" name="csv expe_2"/>
    <field editable="1" name="csv expe_3"/>
    <field editable="1" name="csv expe_4"/>
    <field editable="1" name="csv expe_5"/>
    <field editable="1" name="csv expe_6"/>
    <field editable="1" name="csv expe_7"/>
    <field editable="1" name="csv experi"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_car_psafe"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_car_psafe_l"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_ebike_psafe"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_ebike_psafe_l"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_escoot_psafe"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_escoot_psafe_l"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_from1"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_id"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_length"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_to1"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_walk_psafe"/>
    <field editable="0" name="csv experimental_field_athens_links_psafe_walk_psafe_l"/>
    <field editable="1" name="freespeed"/>
    <field editable="1" name="id"/>
    <field editable="1" name="inf"/>
    <field editable="1" name="length"/>
    <field editable="1" name="modes"/>
    <field editable="1" name="obst"/>
    <field editable="1" name="oneway"/>
    <field editable="1" name="pav"/>
    <field editable="1" name="permlanes"/>
    <field editable="1" name="sl"/>
    <field editable="1" name="x_end"/>
    <field editable="1" name="x_start"/>
    <field editable="1" name="y_end"/>
    <field editable="1" name="y_start"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="capacity"/>
    <field labelOnTop="0" name="cross"/>
    <field labelOnTop="0" name="csv expe_1"/>
    <field labelOnTop="0" name="csv expe_2"/>
    <field labelOnTop="0" name="csv expe_3"/>
    <field labelOnTop="0" name="csv expe_4"/>
    <field labelOnTop="0" name="csv expe_5"/>
    <field labelOnTop="0" name="csv expe_6"/>
    <field labelOnTop="0" name="csv expe_7"/>
    <field labelOnTop="0" name="csv experi"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_car_psafe"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_car_psafe_l"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_ebike_psafe"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_ebike_psafe_l"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_escoot_psafe"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_escoot_psafe_l"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_from1"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_id"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_length"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_to1"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_walk_psafe"/>
    <field labelOnTop="0" name="csv experimental_field_athens_links_psafe_walk_psafe_l"/>
    <field labelOnTop="0" name="freespeed"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="inf"/>
    <field labelOnTop="0" name="length"/>
    <field labelOnTop="0" name="modes"/>
    <field labelOnTop="0" name="obst"/>
    <field labelOnTop="0" name="oneway"/>
    <field labelOnTop="0" name="pav"/>
    <field labelOnTop="0" name="permlanes"/>
    <field labelOnTop="0" name="sl"/>
    <field labelOnTop="0" name="x_end"/>
    <field labelOnTop="0" name="x_start"/>
    <field labelOnTop="0" name="y_end"/>
    <field labelOnTop="0" name="y_start"/>
  </labelOnTop>
  <reuseLastValue>
    <field reuseLastValue="0" name="capacity"/>
    <field reuseLastValue="0" name="cross"/>
    <field reuseLastValue="0" name="freespeed"/>
    <field reuseLastValue="0" name="id"/>
    <field reuseLastValue="0" name="inf"/>
    <field reuseLastValue="0" name="length"/>
    <field reuseLastValue="0" name="modes"/>
    <field reuseLastValue="0" name="obst"/>
    <field reuseLastValue="0" name="oneway"/>
    <field reuseLastValue="0" name="pav"/>
    <field reuseLastValue="0" name="permlanes"/>
    <field reuseLastValue="0" name="x_end"/>
    <field reuseLastValue="0" name="x_start"/>
    <field reuseLastValue="0" name="y_end"/>
    <field reuseLastValue="0" name="y_start"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
