depends = ('ITKPyBase', 'ITKSmoothing', 'ITKImageSources', 'ITKImageGrid', 'ITKIOImageBase', 'ITKCommon', )
templates = (  ('ParameterObject', 'elastix::ParameterObject', 'elastixParameterObject', False),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodIF2IF2', False, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodIF3IF3', False, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodIF4IF4', False, 'itk::Image< float,4 >, itk::Image< float,4 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodID2ID2', False, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodID3ID3', False, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodID4ID4', False, 'itk::Image< double,4 >, itk::Image< double,4 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterIF2', False, 'itk::Image< float,2 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterIF3', False, 'itk::Image< float,3 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterIF4', False, 'itk::Image< float,4 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterID2', False, 'itk::Image< double,2 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterID3', False, 'itk::Image< double,3 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterID4', False, 'itk::Image< double,4 >'),
)
factories = ()
