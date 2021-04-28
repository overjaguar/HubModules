#include "research.h"

std::map<IEE_DataChannel_t, std::string>* Research::signalToString = nullptr;

Research::Research(bool* flags)
{
  signalToString = new std::map<IEE_DataChannel_t, std::string>();
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_AF3, "AF3"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_AF4, "AF3"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_F7, "F7"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_F8, "F8"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_F3, "F3"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_F4, "F4"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_FC5, "FC5"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_FC6, "FC6"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_T7, "T7"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_T8, "T8"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_P7, "P7"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_P8, "P8"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_O1, "O1"));
  signalToString->insert(std::pair<IEE_DataChannel_t, std::string>(IED_O2, "O2"));

  eEvent = IEE_EmoEngineEventCreate();
  eState = IEE_EmoStateCreate();
  std::cout << "INIT RESEARCH" << std::endl;
  this->flags = flags;
  std::string time(filename_time());

  mkdir("modules/EmotivEEG/log", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

  if (flags[MOTION]) {
    //filenames[MOTION] = time+".EmotivEEG-motion.csv";
    ofs[MOTION] = std::ofstream(filenames[MOTION].c_str(), std::ios::trunc);
  }

  if (flags[EEG]) {
    filenames[EEG] = "modules/EmotivEEG/log/" + time+".EmotivEEG-eeg.csv";
    std::cout << "Results of EEG are saved in: " + filenames[EEG] << std::endl;
    ofs[EEG] = std::ofstream(filenames[EEG].c_str(), std::ios::trunc);
  }

  if (flags[FACIAL]){
    filenames[FACIAL] = "modules/EmotivEEG/log/" + time+".EmotivEEG-facial.csv";
    std::cout << "Results of Facial are saved in: " + filenames[FACIAL] << std::endl;
    ofs[FACIAL] = std::ofstream(filenames[FACIAL].c_str(), std::ios::trunc);
  }

  write_headers();

  std::cout << "Motion: " << this->flags[MOTION] << std::endl;
  std::cout << "Waves: " << this->flags[EEG] << std::endl;
  std::cout << "Expression: " << this->flags[FACIAL] << std::endl;
  std::cout << "Test: " << this->flags[TEST] << std::endl;
}

Research::~Research()
{
  IEE_EngineDisconnect();
  IEE_EmoStateFree(eState);
  IEE_EmoEngineEventFree(eEvent);

  if (flags[MOTION]) ofs[MOTION].close();
  if (flags[EEG]) ofs[EEG].close();
  if (flags[FACIAL]) ofs[FACIAL].close();
}

int Research::run()
{
  try {
    if (IEE_EngineConnect() != EDK_OK)
      throw std::runtime_error("Emotiv Driver start up failed.");

    std::cout << "Start receiving EmoState! Press any key to stop logging..." << std::endl;

    std::unique_ptr<void, void (*)(DataHandle)> hMotionData(IEE_MotionDataCreate(), &IEE_MotionDataFree);
    IEE_MotionDataSetBufferSizeInSec(secs);

    while (!_kbhit()) {
      state = IEE_EngineGetNextEvent(eEvent);

      if (state == EDK_OK) {
        eventType = IEE_EmoEngineEventGetType(eEvent);
//        std::cout << IEE_EmoEngineEventGetUserId(eEvent, &userID) << std::endl;

        logEEG();
        logFacial();
        logMotion(&hMotionData);
      } else if (state != EDK_NO_EVENT) {
        std::cout << "Internal error in Emotiv Engine!" << std::endl;
        break;
      }
#ifdef _WIN32
      Sleep(1);
#endif
#if __linux__ || __APPLE__
      usleep(10000);
#endif
    }
  }
  catch (const std::runtime_error& e) {
    std::cerr << e.what() << std::endl;
    std::cout << "Press any key to exit..." << std::endl;
    getchar();
  }

  return 0;
}

std::string Research::filename_time() {
  std::time_t t = std::time(nullptr);
  char mbstr[100];
  if (std::strftime(mbstr, sizeof(mbstr), "%d_%m_%Y_%H_%M_%S", std::localtime(&t))) {
     std::cout << mbstr << std::endl;
  }
  return std::string(mbstr);
}

void Research::write_headers() {
  if(flags[FACIAL]) {
    //ofs[FACIAL] << "Time,";
    //ofs[FACIAL] << "Blink,";
    //ofs[FACIAL] << "Wink Left,";
    //ofs[FACIAL] << "Wink Right,";
    //ofs[FACIAL] << "Surprise,";
    //ofs[FACIAL] << "Frown,";
    //ofs[FACIAL] << "Smile,";
    //ofs[FACIAL] << "Clench";
    //ofs[FACIAL] << std::endl;
  }
  if(flags[MOTION]) {
    const char header[] = "Time, COUNTER, GYROX, GYROY, GYROZ, ACCX, ACCY, ACCZ, MAGX, "
        "MAGY, MAGZ, TIMESTAMP";
    ofs[MOTION] << header << std::endl;
  }
  if(flags[EEG]) {
    //const char header[] = "Time, Theta, Alpha, Low_beta, High_beta, Gamma";
    //ofs[EEG] << header << std::endl;
  }
}

void Research::logFacial() {
  if(!flags[FACIAL]) return;
  if (eventType != IEE_EmoStateUpdated) return;

  IEE_EmoEngineEventGetEmoState(eEvent, eState);

  //Time
  std::time_t t = std::time(nullptr);
  char mbstr[100];
  std::strftime(mbstr, sizeof(mbstr), "%Y-%m-%d %H:%M:%S", std::localtime(&t));
  std::cout << "Facial Time: " << mbstr << " ";
  ofs[FACIAL] << mbstr << ",";

  // FacialExpression Suite results
  ofs[FACIAL] << IS_FacialExpressionIsBlink(eState) << ",";
  std::cout << "B: " << IS_FacialExpressionIsBlink(eState) << " ";

  ofs[FACIAL] << IS_FacialExpressionIsLeftWink(eState) << ",";
  std::cout << "LW: " << IS_FacialExpressionIsLeftWink(eState) << " ";

  ofs[FACIAL] << IS_FacialExpressionIsRightWink(eState) << ",";
  std::cout << "RW: " << IS_FacialExpressionIsRightWink(eState) << " ";

  std::map<IEE_FacialExpressionAlgo_t, float> expressivStates;

  IEE_FacialExpressionAlgo_t upperFaceAction = IS_FacialExpressionGetUpperFaceAction(eState);
  float upperFacePower = IS_FacialExpressionGetUpperFaceActionPower(eState);

  IEE_FacialExpressionAlgo_t lowerFaceAction = IS_FacialExpressionGetLowerFaceAction(eState);
  float lowerFacePower = IS_FacialExpressionGetLowerFaceActionPower(eState);

  expressivStates[ upperFaceAction ] = upperFacePower;
  expressivStates[ lowerFaceAction ] = lowerFacePower;

  ofs[FACIAL] << expressivStates[ FE_SURPRISE] << ","; // eyebrow
  std::cout << "EB: " << expressivStates[ FE_SURPRISE] << " ";

  ofs[FACIAL] << expressivStates[ FE_FROWN   ] << ","; // furrow
  std::cout << "F: " << expressivStates[ FE_FROWN   ] << " ";

  ofs[FACIAL] << expressivStates[ FE_SMILE   ] << ","; // smile
  std::cout << "S: " << expressivStates[ FE_SMILE   ] << " ";

  ofs[FACIAL] << expressivStates[ FE_CLENCH  ] << ","; // clench  
  std::cout << "C: " << expressivStates[ FE_CLENCH   ] << std::endl;
//  FE_NEUTRAL    = 0x0001,
//  FE_BLINK      = 0x0002,
//  FE_WINK_LEFT  = 0x0004,
//  FE_WINK_RIGHT = 0x0008,
//  FE_HORIEYE    = 0x0010,
//  FE_SURPRISE   = 0x0020,
//  FE_FROWN      = 0x0040,
//  FE_SMILE      = 0x0080,
//  FE_CLENCH     = 0x0100,

//FE_LAUGH      = 0x0200,
//FE_SMIRK_LEFT = 0x0400,
//FE_SMIRK_RIGHT= 0x0800

  ofs[FACIAL] << std::endl;
  ofs[FACIAL].flush();
}

void Research::logMotion(std::unique_ptr<void, void (*)(DataHandle)>* hMotionData) {
  if(!flags[MOTION]) return;
  if (eventType != IEE_UserAdded) return;
  std::cout << "Get motion data" << std::endl;
  const IEE_MotionDataChannel_t targetChannelList[] = {
      IMD_COUNTER,
      IMD_GYROX,
      IMD_GYROY,
      IMD_GYROZ,
      IMD_ACCX,
      IMD_ACCY,
      IMD_ACCZ,
      IMD_MAGX,
      IMD_MAGY,
      IMD_MAGZ,
      IMD_TIMESTAMP
  };

  IEE_MotionDataUpdateHandle(userID, hMotionData->get());
  unsigned int nSamplesTaken=0;
  IEE_MotionDataGetNumberOfSample(hMotionData->get(), &nSamplesTaken);

  if (nSamplesTaken != 0) {
    std::cout << "Updated " << nSamplesTaken << std::endl;

    std::vector<double> data(nSamplesTaken);
    ofs[MOTION] << time(NULL) << ",";
    for(int sampleIdx=0 ; sampleIdx<(int)nSamplesTaken ; ++sampleIdx) {
      for(int i = 0; i<sizeof(targetChannelList)/sizeof(IEE_MotionDataChannel_t); i++) {
        IEE_MotionDataGet(hMotionData->get(), targetChannelList[i], data.data(), data.size());
        ofs[MOTION] << data[sampleIdx] << ",";
      }
      ofs[MOTION] << std::endl;
    }
  }
}

void Research::logEEG() {
  if(!flags[EEG]) return;
//  if (eventType != IEE_UserAdded) return;

  std::cout << "Get the average band power" << std::endl;
  IEE_FFTSetWindowingType(userID, IEE_HAMMING);

  //Time
  std::time_t t = std::time(nullptr);
  char mbstr[100];
  std::strftime(mbstr, sizeof(mbstr), "%Y-%m-%d %H:%M:%S", std::localtime(&t));

  IEE_DataChannel_t channelList[] = { IED_AF3, IED_AF4,
                                      IED_F7, IED_F8,
                                      IED_F3, IED_F4,
                                      IED_FC5, IED_FC6,
                                      IED_T7, IED_T8,
                                      IED_P7, IED_P8,
                                      IED_O1, IED_O2 };
  double alpha, low_beta, high_beta, gamma, theta;
  alpha = low_beta = high_beta = gamma = theta = 0;

  double alphaAvg, lowBetaAvg, highBetaAvg, gammaAvg, thetaAvg;
  alphaAvg = lowBetaAvg = highBetaAvg = gammaAvg = thetaAvg = 0;

  int numOfChannels = sizeof(channelList)/sizeof(channelList[0]);

  for(int i=0 ; i < numOfChannels; ++i)
  {
    int result = IEE_GetAverageBandPowers(userID, channelList[i], &theta, &alpha,
                                     &low_beta, &high_beta, &gamma);
    if(result != EDK_OK) continue;

    ofs[EEG] << mbstr << ",";
    ofs[EEG] << theta << ",";
    ofs[EEG] << alpha << ",";
    ofs[EEG] << low_beta << ",";
    ofs[EEG] << high_beta << ",";
    ofs[EEG] << gamma << ",";
    ofs[EEG] << signalToString->at(channelList[i]) << ",";
    ofs[EEG] << std::endl;

    alphaAvg += alpha;
    thetaAvg += theta;
    lowBetaAvg += low_beta;
    highBetaAvg += high_beta;
    gammaAvg += gamma;
  }

  alphaAvg /= numOfChannels;
  thetaAvg /= numOfChannels;
  lowBetaAvg /= numOfChannels;
  highBetaAvg /= numOfChannels;
  gammaAvg /= numOfChannels;

  ofs[EEG] << mbstr << ",";
  ofs[EEG] << thetaAvg << ",";
  ofs[EEG] << alphaAvg << ",";
  ofs[EEG] << lowBetaAvg << ",";
  ofs[EEG] << highBetaAvg << ",";
  ofs[EEG] << gammaAvg << ",";
  ofs[EEG] << "Average" << ",";
  ofs[EEG] << std::endl;

  std::cout << "EEG Time: " << mbstr << " ";
  std::cout << "Theta: " << thetaAvg << " ";
  std::cout << "Alpha: " << alphaAvg << " ";
  std::cout << "LowBeta: " << lowBetaAvg << " ";
  std::cout << "HighBeta: " << highBetaAvg << " ";
  std::cout << "Gamma: " << gammaAvg << std::endl;
}

#ifdef __linux__
int Research::_kbhit(void)
{
    struct timeval tv;
    fd_set read_fd;

    tv.tv_sec=0;
    tv.tv_usec=0;

    FD_ZERO(&read_fd);
    FD_SET(0,&read_fd);

    if(select(1, &read_fd, NULL, NULL, &tv) == -1)
    return 0;

    if(FD_ISSET(0,&read_fd))
        return 1;

    return 0;
}
#endif
#ifdef __APPLE__
int Research::_kbhit(void)
{
    struct timeval tv;
    fd_set rdfs;

    tv.tv_sec = 0;
    tv.tv_usec = 0;

    FD_ZERO(&rdfs);
    FD_SET (STDIN_FILENO, &rdfs);

    select(STDIN_FILENO+1, &rdfs, NULL, NULL, &tv);
    return FD_ISSET(STDIN_FILENO, &rdfs);
}
#endif
