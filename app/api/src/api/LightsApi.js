/**
 * OralEye API
 * API for controlling lights and camera on OralEye device
 *
 * The version of the OpenAPI document: 0.0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */


import ApiClient from "../ApiClient";
import LightsBlueMaxTimePostRequest from '../model/LightsBlueMaxTimePostRequest';
import LightsControlPost200Response from '../model/LightsControlPost200Response';
import LightsStatusGet200Response from '../model/LightsStatusGet200Response';

/**
* Lights service.
* @module api/LightsApi
* @version 0.0.1
*/
export default class LightsApi {

    /**
    * Constructs a new LightsApi. 
    * @alias module:api/LightsApi
    * @class
    * @param {module:ApiClient} [apiClient] Optional API client implementation to use,
    * default to {@link module:ApiClient#instance} if unspecified.
    */
    constructor(apiClient) {
        this.apiClient = apiClient || ApiClient.instance;
    }


    /**
     * Callback function to receive the result of the lightsBlueMaxTimePost operation.
     * @callback module:api/LightsApi~lightsBlueMaxTimePostCallback
     * @param {String} error Error message, if any.
     * @param {module:model/LightsControlPost200Response} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Set blue light maximum on time for health safety
     * @param {module:model/LightsBlueMaxTimePostRequest} lightsBlueMaxTimePostRequest 
     * @param {module:api/LightsApi~lightsBlueMaxTimePostCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:model/LightsControlPost200Response}
     */
    lightsBlueMaxTimePost(lightsBlueMaxTimePostRequest, callback) {
      let postBody = lightsBlueMaxTimePostRequest;
      // verify the required parameter 'lightsBlueMaxTimePostRequest' is set
      if (lightsBlueMaxTimePostRequest === undefined || lightsBlueMaxTimePostRequest === null) {
        throw new Error("Missing the required parameter 'lightsBlueMaxTimePostRequest' when calling lightsBlueMaxTimePost");
      }

      let pathParams = {
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = ['application/json'];
      let accepts = ['application/json'];
      let returnType = LightsControlPost200Response;
      return this.apiClient.callApi(
        '/lights/blue/max_time', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the lightsControlPost operation.
     * @callback module:api/LightsApi~lightsControlPostCallback
     * @param {String} error Error message, if any.
     * @param {module:model/LightsControlPost200Response} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Set lights on/off
     * @param {module:model/LightsStatusGet200Response} lightsStatusGet200Response 
     * @param {module:api/LightsApi~lightsControlPostCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:model/LightsControlPost200Response}
     */
    lightsControlPost(lightsStatusGet200Response, callback) {
      let postBody = lightsStatusGet200Response;
      // verify the required parameter 'lightsStatusGet200Response' is set
      if (lightsStatusGet200Response === undefined || lightsStatusGet200Response === null) {
        throw new Error("Missing the required parameter 'lightsStatusGet200Response' when calling lightsControlPost");
      }

      let pathParams = {
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = ['application/json'];
      let accepts = ['application/json'];
      let returnType = LightsControlPost200Response;
      return this.apiClient.callApi(
        '/lights/control', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the lightsStatusGet operation.
     * @callback module:api/LightsApi~lightsStatusGetCallback
     * @param {String} error Error message, if any.
     * @param {module:model/LightsStatusGet200Response} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Get status of the lights
     * @param {module:api/LightsApi~lightsStatusGetCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:model/LightsStatusGet200Response}
     */
    lightsStatusGet(callback) {
      let postBody = null;

      let pathParams = {
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = LightsStatusGet200Response;
      return this.apiClient.callApi(
        '/lights/status', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }


}
